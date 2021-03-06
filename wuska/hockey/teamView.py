from wuska.hockey.models import *
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from wuska.hockey.forms import *
from django.db.models import Q
from django.contrib.auth.models import User
from wuska.accounts.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

@login_required
def viewTeam(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    return render_to_response('hockey/viewTeam.html', {'team':team, 'user':request.user,'profile':request.user.get_profile(),'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage(request.user.id,team.owner,team.general_manager1,team.general_manager2),'owner':is_owner(team.owner,request.user.id),'contract_status_change':team.contract_status_change}, context_instance=RequestContext(request))

def getPlayer(p_id):
    if p_id == -1:
        return "Empty!"
    else:
        return get_object_or_404(Player, pk = p_id)

@login_required
def createTeam(request):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            abbreviation = cd['abbreviation']
            arena_name = cd['arena_name']           
            arena = Arena(name=arena_name, occupancy=5000, practice_facility=0,locker_room=0, equipment=0, rink=0, concessions=0, lower_bowl=1, mid_bowl=0, upper_bowl=0, box=0, ticket_lower=5, ticket_mid=2, ticket_upper=1, ticket_box=10)
            arena.save()
            team = Team(name=name, owner=request.user.id, general_manager1=-1,general_manager2=-1, league_id=-1,arena=arena,funds=2000000, salary_used=0, salary_left=2000000,numLWNeed=4,numCNeed=4,numRWNeed=4,numDNeed=6,numGNeed=2,avgAge=00.000, contract_status_change=False)
            team.save()
            request.user.get_profile().teams_owned.add(team)
            request.user.get_profile().teams.add(team)   
            #find out how many teams in game after creating this team
            num_teams = Team.objects.all().count()
            if num_teams % 30 == 1:#then team just added will not fit into existing leagues, so create a new league
                num_leagues = League.objects.all().count()
                league = League(name='League %s'%(num_leagues + 1),salary_cap = 8000000)
                league.save()
            #get the last created League and add team to it
            league = League.objects.order_by('-pk')[0]
            league.teams.add(team)
            if league.division1.count() < 5:
                league.division1.add(team)
            elif league.division2.count() < 5:
                league.division2.add(team)
            elif league.division3.count() < 5:
                league.division3.add(team)
            elif league.division4.count() < 5:
                league.division4.add(team)
            elif league.division5.count() < 5:
                league.division5.add(team)
            elif league.division6.count() < 5:
                league.division6.add(team)
            else:
                raise Exception("League is full when it shouldn't be. Please post on the support page about this issue or notify an admin so that we can quickly fix this issue for you!")
            league.save()
            team.league_id = league.id
            team.save()
            next = "/team/%s/"%(team.pk)
            return redirect(next)
    else:
        form = TeamForm()
    return render_to_response('hockey/createTeam.html',{'form':form, 'user':request.user, 'profile':request.user.get_profile(),'player_list':player_list, 'team_list':team_list}, context_instance=RequestContext(request))

@login_required
def offerPlayerContract(request, player_id):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    player = get_object_or_404(Player, pk=player_id)
    owner = False
    if player_list.filter(pk=player_id).count() is 1:
        owner = True
    can_manage = False
    if team_list.count()>0:
        can_manage = True
    if request.method == 'POST' and can_manage:
        form = OfferPlayerContractForm(request.POST)
        if form.is_valid() and player.free_agent:
            cd = form.cleaned_data
            salary = cd['salary']
            length = cd['length']
            no_trade = cd['no_trade']
            message = cd['message']
            team_id = request.POST['team']
            team = get_object_or_404(Team, pk=team_id)
            contract = Contract(player_id=player_id, team_id=team_id, team_name=team.name, salary=salary, length = length,no_trade=no_trade, message=message, is_accepted=False)
            contract.save()
            #player should only have 1 contract offer per team.
            for c in player.contracts.all():
                if c.team_id == team.id:
                    c.delete()
            team.contracts.add(contract)
            team.save()
            player.contracts.add(contract)
            player.new_contract = True
            player.save()

            #send an automated message to the player informing them of contract
            title = "New Contract Offer For %s" % (player.name)
            body = "Team %s has offered %s a contract worth %s per season for %s season(s)" % (team.name,player.name,salary,length)
            sender_cc_users =[]
            if team.general_manager1 != -1:
                sender_cc_users.append(get_object_or_404(UserProfile,pk=team.general_manager1))
            if team.general_manager2 != -1:
                sender_cc_users.append(get_object_or_404(UserProfile,pk=team.general_manager2))
            concerning_players = [player]
            receiver_users = [get_object_or_404(UserProfile,pk=player.user_id)]
            send_message(title,body,team.owner,sender_cc_users,-1,team.id,concerning_players,[],receiver_users,True)

            owner = True if request.user.id == team.owner else False
            alert = "You have offered a contract to %s" % (player.name)
            return render_to_response('hockey/viewTeam.html', {'team':team, 'user':request.user,'profile':request.user.get_profile(),'player_list':player_list,'player':player,'team_list':team_list,'alert_success':True,'alert_message':alert,'can_manage':True,'owner':owner}, context_instance=RequestContext(request))
        else:
            form = OfferPlayerContractForm(request.POST)
    else:
        form = OfferPlayerContractForm()
    return render_to_response('hockey/offerPlayerContract.html',{'form':form, 'user':request.user, 'profile':request.user.get_profile(),'player_list':player_list,'player':player,'player_name':player.name,'team_list':team_list,'can_manage':can_manage,'show_manage':True,'owner':owner,'is_free_agent':player.free_agent,'contract_end':player.contract_end,'player_id':player.id}, context_instance=RequestContext(request))

@login_required
def message_players_on_team(request,team_id):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    team = get_object_or_404(Team, pk=team_id)
    can_manage2 = can_manage(request.user.id,team.owner,team.general_manager1,team.general_manager2)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            title = cd['title']
            body = cd['body']
            sender_cc_users = []
            # Add the other team management members to the message
            if request.user.id == team.owner:
                if team.general_manager1 != -1:
                    sender_cc_users.append(get_object_or_404(UserProfile,pk=team.general_manager1))
                if team.general_manager2 != -1:
                    sender_cc_users.append(get_object_or_404(UserProfile,pk=team.general_manager2))
            elif request.user.id == team.general_manager1:
                sender_cc_users.append(get_object_or_404(UserProfile,pk=team.owner))
                if team.general_manager2 != -1:
                    sender_cc_users.append(get_object_or_404(UserProfile,pk=team.general_manager2))
            elif request.user.id == team.general_manager2:
                sender_cc_users.append(get_object_or_404(UserProfile,pk=team.owner))
                if team.general_manager1 != -1:
                    sender_cc_users.append(get_object_or_404(UserProfile,pk=team.general_manager1))            
            concerning_players = []
            receiver_users = []
            for player in team.players.all():
                concerning_players.append(player)
                receiver_users.append(get_object_or_404(UserProfile,pk=player.user_id))

            send_message(title,body,request.user.id,sender_cc_users,-1,team.id,concerning_players,[],receiver_users,False)

            alert="Message sent to all players on the team."
            return render_to_response('hockey/viewTeam.html', {'team':team, 'user':request.user,'profile':request.user.get_profile(),'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage2,'alert_success':True,'alert_message':alert,'owner':is_owner(team.owner,request.user.id)}, context_instance=RequestContext(request))
        else:
            form = MessageForm(request.POST)
    else:
        form = MessageForm()
    return render_to_response('hockey/messagePlayersOnTeam.html',{'form':form, 'user':request.user, 'profile':request.user.get_profile(),'player_list':player_list, 'team_list':team_list,'team':team, 'can_manage':can_manage2,'owner':is_owner(team.owner,request.user.id)}, context_instance=RequestContext(request))


@login_required
def editLines(request, team_id):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    t = get_object_or_404(Team, pk=team_id)
    t_players = t.players
    if request.method == 'POST':
        form_get = make_edit_lines_form(t_players)
        form = form_get(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            lw1 = cd['l1_field']
            c1 = cd['c1_field']
            rw1 = cd['r1_field']
            d1 = cd['d1_field']
            g1 = cd['g1_field']
            lw2 = cd['l2_field']
            c2 = cd['c2_field']
            rw2 = cd['r2_field']
            d2 = cd['d2_field']
            g2 = cd['g2_field']
            lw3 = cd['l3_field']
            c3 = cd['c3_field']
            rw3 = cd['r3_field']
            d3 = cd['d3_field']
            lw4 = cd['l4_field']
            c4 = cd['c4_field']
            rw4 = cd['r4_field']
            d4 = cd['d4_field']
            d5 = cd['d5_field']
            d6 = cd['d6_field']
            pp1l = cd['pp1l_field']
            pp1c = cd['pp1c_field']
            pp1r = cd['pp1r_field']
            pp1ld = cd['pp1ld_field']
            pp1rd = cd['pp1rd_field']
            pp2l = cd['pp2l_field']
            pp2c = cd['pp2c_field']
            pp2r = cd['pp2r_field']
            pp2ld = cd['pp2ld_field']
            pp2rd = cd['pp2rd_field']
            pk1c = cd['pk1c_field']
            pk1w = cd['pk1w_field']
            pk1ld = cd['pk1ld_field']
            pk1rd = cd['pk1rd_field']
            pk2c = cd['pk2c_field']
            pk2w = cd['pk2w_field']
            pk2ld = cd['pk2ld_field']
            pk2rd = cd['pk2rd_field']


            if player_id_in_team(lw1,t_players):
                t.lw1 = lw1
                t_players = t_players.exclude(pk = lw1)
            if player_id_in_team(lw2,t_players):
                t.lw2 = lw2
                t_players = t_players.exclude(pk = lw2)
            if player_id_in_team(lw3,t_players):
                t.lw3 = lw3
                t_players = t_players.exclude(pk = lw3)
            if player_id_in_team(lw4,t_players):
                t.lw4 = lw4
                t_players = t_players.exclude(pk = lw4)

            if player_id_in_team(c1,t_players):
                t.c1 = c1
                t_players = t_players.exclude(pk = c1)
            if player_id_in_team(c2,t_players):
                t.c2 = c2
                t_players = t_players.exclude(pk = c2)
            if player_id_in_team(c3,t_players):
                t.c3 = c3
                t_players = t_players.exclude(pk = c3)
            if player_id_in_team(c4,t_players):
                t.c4 = c4
                t_players = t_players.exclude(pk = c4)

            if player_id_in_team(rw1,t_players):
                t.rw1 = rw1
                t_players = t_players.exclude(pk = rw1)
            if player_id_in_team(rw2,t_players):
                t.rw2 = rw2
                t_players = t_players.exclude(pk = rw2)
            if player_id_in_team(rw3,t_players):
                t.rw3 = rw3
                t_players = t_players.exclude(pk = rw3)
            if player_id_in_team(rw4,t_players):
                t.rw4 = rw4
                t_players = t_players.exclude(pk = rw4)

            if player_id_in_team(d1,t_players):
                t.defense1 = d1
                t_players = t_players.exclude(pk = d1)
            if player_id_in_team(d2,t_players):
                t.defense2 = d2
                t_players = t_players.exclude(pk = d2)
            if player_id_in_team(d3,t_players):
                t.defense3 = d3
                t_players = t_players.exclude(pk = d3)
            if player_id_in_team(d4,t_players):
                t.defense4 = d4
                t_players = t_players.exclude(pk = d4)
            if player_id_in_team(d5,t_players):
                t.defense5 = d5
                t_players = t_players.exclude(pk = d5)
            if player_id_in_team(d6,t_players):
                t.defense6 = d6
                t_players = t_players.exclude(pk = d6)

            if player_id_in_team(g1,t_players):
                t.goalie1 = g1
                t_players = t_players.exclude(pk = g1)
            if player_id_in_team(g2,t_players):
                t.goalie2 = g2
                t_players = t_players.exclude(pk = g2)

                #special teams
            pp_players = t.players
            if player_id_in_team(pp1l,pp_players):
                t.pp1lw = pp1l
                pp_players = pp_players.exclude(pk = pp1w)
            if player_id_in_team(pp1c,pp_players):
                t.pp1c = pp1c
                pp_players = pp_players.exclude(pk = pp1c)
            if player_id_in_team(pp1r,pp_players):
                t.pp1rw = pp1r
                pp_players = pp_players.exclude(pk = pp1r)
            if player_id_in_team(pp1ld,pp_players):
                t.pp1ld = pp1ld
                pp_players = pp_players.exclude(pk = pp1ld)
            if player_id_in_team(pp1rd,pp_players):
                t.pp1rd = pp1rd
                pp_players = pp_players.exclude(pk = pp1rd)
                
            if player_id_in_team(pp2l,pp_players):
                t.pp2lw = pp2l
                pp_players = pp_players.exclude(pk = pp2l)
            if player_id_in_team(pp2c,pp_players):
                t.pp2c = pp2c
                pp_players = pp_players.exclude(pk = pp2c)
            if player_id_in_team(pp2r,pp_players):
                t.pp2rw = pp2r
                pp_players = pp_players.exclude(pk = pp2r)
            if player_id_in_team(pp2ld,pp_players):
                t.pp2ld = pp2ld
                pp_players = pp_players.exclude(pk = pp2ld)
            if player_id_in_team(pp2rd,pp_players):
                t.pp2rd = pp2rd
                pp_players = pp_players.exclude(pk = pp2rd)

                #Penalty Kill
            pp_players = t.players
            if player_id_in_team(pk1w,pp_players):
                t.pk1w = pk1w
                pp_players = pp_players.exclude(pk = pk1w)
            if player_id_in_team(pk1c,pp_players):
                t.pk1c = pk1c
                pp_players = pp_players.exclude(pk = pk1c)
            if player_id_in_team(pk1ld,pp_players):
                t.pk1ld = pk1ld
                pp_players = pp_players.exclude(pk = pk1ld)
            if player_id_in_team(pk1rd,pp_players):
                t.pk1rd = pk1rd
                pp_players = pp_players.exclude(pk = pk1rd)

            if player_id_in_team(pk2w,pp_players):
                t.pk2w = pk2w
                pp_players = pp_players.exclude(pk = pk2w)
            if player_id_in_team(pk2c,pp_players):
                t.pk2c = pk2c
                pp_players = pp_players.exclude(pk = pk2c)
            if player_id_in_team(pk2ld,pp_players):
                t.pk2ld = pk2ld
                pp_players = pp_players.exclude(pk = pk2ld)
            if player_id_in_team(pk2rd,pp_players):
                t.pk2rd = pk2rd
                pp_players = pp_players.exclude(pk = pk2rd)

            t.save()
            next = "/team/%s"%(t.pk)
            return redirect(next)
    else:
        form = make_edit_lines_form(t_players)
    return render_to_response('hockey/editLines.html',{'form':form, 'team':t,'user':request.user, 'profile':request.user.get_profile(),'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage(request.user.id,t.owner,t.general_manager1,t.general_manager2),'owner':is_owner(t.owner,request.user.id)}, context_instance=RequestContext(request))

@login_required
def teamViewMessagesRedirect(request, team_id):
    return redirect('/team/%s/viewMessages/received/10'%(team_id))
@login_required
def teamViewMessages(request, team_id, last_message,sent_or_rec):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    team = get_object_or_404(Team, pk=team_id)
    sent = False
    if sent_or_rec == "sent":
        sent = True
    can_manage2 = can_manage(request.user.id,team.owner, team.general_manager1,team.general_manager2)
    if can_manage2:
        team.new_message = False
        team.save()
        last_message = int(last_message)
        newer_message = last_message - 10
        older_message = last_message + 10
        have_new_messages = False
        have_older_messages = True
        num_messages = team.messages.count()
        if older_message >= num_messages:
            have_older_messages = False
        if last_message <10:
            last_message = 10
            newer_message = last_message
        elif last_message > 10:
            have_new_messages = True
        message_list = team.messages.order_by('-id')[(newer_message):last_message]
        from_list = []
        href_list = []
        name_list = []
        for message in message_list:
            if sent:
                if message.receiver_team_id != -1:
                    t = get_object_or_404(Team,pk=message.receiver_team_id)
                    from_list.append("Team: ")
                    href_list.append("/team/%d/"%(t.id))
                    name_list.append(t.name)
                else:
                    from_list.append("Agent: ")
                    href_list.append("/users/%d/"%(message.receiver_user_id))
                    rec_user = get_object_or_404(User,pk=message.receiver_user_id)
                    name_list.append(rec_user.username) 
            else:
                if message.receiver_team_id == team_id:
                    if message.sender_player_id != -1:
                        p = get_object_or_404(Player,pk=message.sender_player_id)
                        from_list.append("Player: ")
                        href_list.append("/player/%d/"%(p.id))
                        name_list.append(p.name)
                    elif message.sender_team_id != -1 and message.sender_team_id != team.id:
                        t = get_object_or_404(Team,pk=message.sender_team_id)
                        from_list.append("Team: ")
                        href_list.append("/team/%d/"%(t.id))
                        name_list.append(t.name)
                    elif message.sender_user_id != -1:
                        from_list.append("Agent: ")
                        href_list.append("/users/%d/"%(message.sender_user_id))
                        user = get_object_or_404(User,pk=message.sender_user_id)
                        name_list.append(user.username)            
        m_list = zip(message_list,from_list,href_list,name_list)  
        return render_to_response('hockey/teamViewMessages.html', {'team': team, 'user':request.user, 'profile':request.user.get_profile(),'player_list':player_list, 'team_list':team_list,'can_manage':can_manage2,'message_list':m_list,'older_message':older_message,'newer_message':newer_message,'have_new_messages':have_new_messages,'have_older_messages':have_older_messages,'sent':sent,'owner':is_owner(team.owner,request.user.id)},context_instance=RequestContext(request))
    return redirect('/team/%s/'%(team_id))  #not a team manager


@login_required
def message_team_management(request,team_id):
    profile = request.user.get_profile()
    player_list = profile.players.all()
    team_list = profile.teams.all()
    team = get_object_or_404(Team, pk=team_id)
    can_manage2 = can_manage(request.user.id,team.owner,team.general_manager1,team.general_manager2)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            title = cd['title']
            body = cd['body']
            receiver_users = [get_object_or_404(UserProfile,pk=team.owner)]
            if team.general_manager1 != -1:
                gm1_profile = get_object_or_404(UserProfile,pk=team.general_manager1)
                receiver_users.append(gm1_profile)
            if team.general_manager2!= -1:
                gm2_profile = get_object_or_404(UserProfile,pk=team.general_manager2)
                receiver_users.append(gm2_profile)
            send_message(title,body,request.user.id,[],-1,-1,[],[team],receiver_users,False)
            alert="Message sent to the management of %s." % (team.name)
            return render_to_response('hockey/viewTeam.html', {'team':team, 'user':request.user,'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage2,'alert_success':True,'alert_message':alert,'owner':is_owner(team.owner,request.user.id)}, context_instance=RequestContext(request))
        else:
            form = MessageForm(request.POST)
    else:
        form = MessageForm()
    return render_to_response('hockey/messageTeamManagement.html',{'form':form, 'user':request.user, 'player_list':player_list, 'team_list':team_list,'team':team, 'can_manage':can_manage2,'owner':is_owner(team.owner,request.user.id)}, context_instance=RequestContext(request))

@login_required
def viewContracts(request,team_id):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    team = get_object_or_404(Team, pk=team_id)
    can_manage2 = can_manage(request.user.id,team.owner,team.general_manager1,team.general_manager2)
    if can_manage2:
        team.contract_status_change = False
        team.save()
        name_list = []
        contracts = team.contracts.all()
        position_list = []
        for contract in contracts:
            p = get_object_or_404(Player,pk=contract.player_id)
            name_list.append(p.name)
            position_list.append(p.position)
        contract_list = zip(contracts,name_list,position_list)
        return render_to_response('hockey/viewContractOffersTeam.html', {'team':team, 'user':request.user,'profile':request.user.get_profile(),'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage2,'contract_list':contract_list,'owner':is_owner(team.owner,request.user.id)}, context_instance=RequestContext(request))
    return redirect('/team/%s/'%(team_id))

@login_required
def viewManagement(request,team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.user.id != team.owner:#only owner should alter management
        return redirect('/team/%s/'%(team_id))
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    try:
        gm1_name = User.objects.get(id=team.general_manager1)
    except ObjectDoesNotExist:
        gm1_name = ""
    try:
        gm2_name = User.objects.get(id=team.general_manager2)
    except ObjectDoesNotExist:
        gm2_name = ""
    if request.method == 'POST':
        form_get = get_management_form(gm1_name,gm2_name,team.owner)
        form = form_get(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            gm1_id = cd['gm1_username']
            gm2_id = cd['gm2_username']

            if gm1_id != team.general_manager1 and team.general_manager1 != -1:
                body = "You are no longer the General Manager of %s."%(team.name)
                title = "No Longer General Manager of %s"%(team.name)
                profile = get_object_or_404(UserProfile,pk=team.general_manager1)
                sender_cc_users = []
                #In future might want to send a copy to team managers
                send_message(title,body,team.owner,sender_cc_users,-1,team.id,[],[team],[profile],True)
                profile.teams_gmed.remove(team)
                profile.teams.remove(team)
                profile.save()
                if gm1_id != -1:#if there is a new GM1
                    body = "Congratulations! You are now the General Manager of %s."%(team.name)
                    title = "General Manager of %s"%(team.name)
                    profile = get_object_or_404(UserProfile,pk=gm1_id)
                    send_message(title,body,team.owner,[],-1,team.id,[],[team],[profile],True)
                    profile.teams_gmed.add(team)
                    profile.teams.add(team)
                    profile.save()
                    
            elif gm1_id != -1 and gm1_id != team.general_manager1:#if not already gm, send msg
                body = "Congratulations! You are now the General Manager of %s."%(team.name)
                title = "General Manager of %s"%(team.name)
                profile = get_object_or_404(UserProfile,pk=gm1_id)
                send_message(title,body,team.owner,[],-1,team.id,[],[team],[profile],True)
                profile.teams_gmed.add(team)
                profile.teams.add(team)
                profile.save()
            
            if gm2_id != team.general_manager2 and team.general_manager2 != -1:
                body = "You are no longer the General Manager of %s."%(team.name)
                title = "No Longer General Manager of %s"%(team.name)
                profile = get_object_or_404(UserProfile,pk=team.general_manager2)
                sender_cc_users = []
                #In future might want to send a copy to team managers
                send_message(title,body,team.owner,sender_cc_users,-1,team.id,[],[team],[profile],True)
                profile.teams_gmed.remove(team)
                profile.teams.remove(team)
                profile.save()
                if gm2_id != -1:
                    body = "Congratulations! You are now the General Manager of %s."%(team.name)
                    title = "General Manager of %s"%(team.name)
                    profile = get_object_or_404(UserProfile,pk=gm2_id)
                    send_message(title,body,team.owner,[],-1,team.id,[],[team],[profile],True)
                    profile.teams_gmed.add(team)
                    profile.teams.add(team)
                    profile.save()

            elif gm2_id != -1 and gm2_id != team.general_manager2:#if not already gm, send msg
                body = "Congratulations! You are now the General Manager of %s."%(team.name)
                title = "General Manager of %s"%(team.name)
                profile = get_object_or_404(UserProfile,pk=gm2_id)
                send_message(title,body,team.owner,[],-1,team.id,[],[team],[profile],True)
                profile.teams_gmed.add(team)
                profile.teams.add(team)
                profile.save()
           
            team.general_manager1 = gm1_id
            team.general_manager2 = gm2_id
            team.save()
            next = "/team/%s"%(team.pk)
            #return redirect(next)
            alert="Management successfully changed."
            return render_to_response('hockey/viewTeam.html', {'team':team, 'user':request.user,'profile':request.user.get_profile(),'player_list':player_list, 'team_list':team_list, 'can_manage':True,'alert_success':True,'alert_message':alert,'owner':True}, context_instance=RequestContext(request))    
        else:
            form = get_management_form(gm1_name,gm2_name,team.owner)
            form = form(request.POST)
    else:
        form = get_management_form(gm1_name,gm2_name,team.owner)
    return render_to_response('hockey/viewManagement.html',{'form':form, 'team':team,'user':request.user,'profile':request.user.get_profile(), 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage(request.user.id,team.owner,team.general_manager1,team.general_manager2),'owner':is_owner(team.owner,request.user.id)}, context_instance=RequestContext(request))
            

def can_manage(request_user_id,team_owner,team_general_manager1,team_general_manager2):
    if request_user_id == team_owner or request_user_id == team_general_manager1 or request_user_id == team_general_manager2:
        return True
    return False
        
def player_id_in_team(p_id,playerlist):
    if playerlist.filter(pk=p_id).count() == 1:
        return True
    return False

def send_message(title,body,sender_user_id,sender_cc_users,sender_player_id,sender_team_id,concerning_players,concerning_teams,receiver_users,is_automated):
    message = Message(sender_user_id=sender_user_id,sender_player_id = sender_player_id,sender_team_id = sender_team_id,title = title, body = body,is_automated=is_automated)
    message.save()
    sender_profile = get_object_or_404(UserProfile,pk=sender_user_id)
    sender_profile.messages.add(message)
    sender_profile.save()
    for user in sender_cc_users:
        message.sender_cc_users.add(user)
        user.messages.add(message)
        user.new_message = True
        user.save()
    for player in concerning_players:
        message.concerning_players.add(player)
    for team in concerning_teams:
        message.concerning_teams.add(team)
    for user in receiver_users:
        message.receiver_users.add(user)
        user.messages.add(message)
        user.new_message = True
        user.save()
    message.save()

def is_owner(team_owner,user_id):
    if (team_owner == user_id):
        return True
    return False
