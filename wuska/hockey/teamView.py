from wuska.hockey.models import *
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from wuska.hockey.forms import *
from django.db.models import Q

@login_required
def viewTeam(request, team_id):
    t = get_object_or_404(Team, pk=team_id)
    player_list = request.user.get_profile().players.all()
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('hockey/viewTeam.html', {'team':t, 'user':request.user,'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage(request.user.id,t.owner,t.general_Manager)}, context_instance=RequestContext(request))

def getPlayer(p_id):
    if p_id == -1:
        return "Empty!"
    else:
        return get_object_or_404(Player, pk= p_id)

@login_required
def createTeam(request):
    player_list = request.user.get_profile().players.all()
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            abbreviation = cd['abbreviation']
            arena_name = cd['arena_name']
            arena = Arena(name=arena_name, occupancy=5000, practice_Facility = 0,locker_Room = 0, equipment = 0, rink = 0, concessions = 0, lower_bowl = 1, mid_bowl = 0, upper_bowl = 0, box = 0, ticket_lower = 5, ticket_mid = 2, ticket_upper = 1, ticket_box = 10)
            arena.save()
            team = Team(name = name, owner=request.user.id, general_Manager=-1, league_id= -1,arena=arena,funds = 2000000, salary_used=0, salary_left=2000000)
            team.save()
            request.user.get_profile().teams.add(team)            
            next = "/team/%s"%(team.pk)
            return redirect(next)
    else:
        form = TeamForm()
    return render_to_response('hockey/createTeam.html',{'form':form, 'user':request.user, 'player_list':player_list, 'team_list':team_list}, context_instance=RequestContext(request))

@login_required
def offerPlayerContract(request, player_id):
    player_list = request.user.get_profile().players.all()
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    if request.method == 'POST':
        form = OfferPlayerContractForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            salary = cd['salary']
            length = cd['length']
            no_trade = cd['no_trade']
            message = cd['message']
            team_id = request.POST['team']
            team = get_object_or_404(Team, pk=team_id)
            team_name = team.name
            contract = Contract(player_id=player_id, team_id=team_id, team_name=team_name, salary=salary, length = length,no_trade=no_trade, message=message, is_accepted=False)
            contract.save()
            team.contracts.add(contract)
            team.save()
            player = get_object_or_404(Player, pk=player_id)
            player.contracts.add(contract)
            player.save()
            can_manage = False
            if request.user.id == team.owner or request.user.id == team.general_manager:
                can_manage = True
            alert = "You have offered a contract to %s" % (player.name)
            return render_to_response('hockey/viewTeam.html', {'team':team, 'user':request.user,'player_list':player_list,'team_list':team_list,'alert_success':True,'alert_message':alert,'can_manage':can_manage}, context_instance=RequestContext(request))

    form = OfferPlayerContractForm(request.POST)
    owner = False
    if player_list.filter(pk=player_id).count() is 1:
        owner = True
    can_manage = False
    if len(team_list)>0:
        can_manage = True
    return render_to_response('hockey/offerPlayerContract.html',{'form':form, 'user':request.user, 'player_list':player_list, 'team_list':team_list,'can_manage':can_manage,'owner':owner}, context_instance=RequestContext(request))

@login_required
def message_players_on_team(request,team_id):
    player_list = request.user.get_profile().players.all()
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    team = get_object_or_404(Team, pk=team_id)
    can_manage2 = can_manage(request.user.id,team.owner,team.general_Manager)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            title = cd['title']
            body = cd['body']
            team_players = team.players
            message = Message(sender_user_id=request.user.id,sender_player_id=-1,sender_team_id=team_id,receiver_team_id=team_id,title=title,body=body)
            message.save()
            message.receiver_players=team_players.all()
            message.save()
            team.messages.add(message)
            team.save()
            for player in team_players.all():
                player.messages.add(message)
                player.save()
            alert="Message sent to all players on the team."
            return render_to_response('hockey/viewTeam.html', {'team':team, 'user':request.user,'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage2,'alert_success':True,'alert_message':alert}, context_instance=RequestContext(request))
    else:
        form = MessageForm(request.POST)
    return render_to_response('hockey/messagePlayersOnTeam.html',{'form':form, 'user':request.user, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage2}, context_instance=RequestContext(request))


@login_required
def editLines(request, team_id):
    player_list = request.user.get_profile().players.all()
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
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

            t.save()
            next = "/team/%s"%(t.pk)
            return redirect(next)
    else:
        form = make_edit_lines_form(t_players)
    return render_to_response('hockey/editLines.html',{'form':form, 'team':t,'user':request.user, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage(request.user.id,t.owner,t.general_Manager)}, context_instance=RequestContext(request))


def can_manage(request_user_id,team_owner, team_general_manager):
    if request_user_id == team_owner or request_user_id == team_general_manager:
        return True
    return False
        
def player_id_in_team(p_id,playerlist):
    if playerlist.filter(pk=p_id).count() == 1:
        return True
    return False
