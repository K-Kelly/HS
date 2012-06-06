from hockey.models import *
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
    goalie1 = getPlayer(t.goalie1)
    goalie2 = getPlayer(t.goalie2)
    defense1 = getPlayer(t.defense1)#2
    defense2 = getPlayer(t.defense2)
    defense3 = getPlayer(t.defense3)
    defense4 = getPlayer(t.defense4)
    defense5 = getPlayer(t.defense5)
    defense6 = getPlayer(t.defense6)
    lw1 = getPlayer(t.lw1)#8
    lw2 = getPlayer(t.lw2)
    lw3 = getPlayer(t.lw3)
    lw4 = getPlayer(t.lw4)
    c1 = getPlayer(t.c1)#12
    c2 = getPlayer(t.c2)
    c3 = getPlayer(t.c3)
    c4 = getPlayer(t.c4)
    rw1 = getPlayer(t.rw1)#16
    rw2 = getPlayer(t.rw2)
    rw3 = getPlayer(t.rw3)
    rw4 = getPlayer(t.rw4)

    current_lines = (goalie2, goalie2, defense1, defense2, defense3, defense4, defense5, defense6, lw1, lw2, lw3, lw4, c1,c2,c3,c4, rw1, rw2, rw3, rw4)
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('hockey/viewTeam.html', {'team':t, 'user':request.user,'current_lines':current_lines, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage(request.user.id,t.owner,t.general_Manager)}, context_instance=RequestContext(request))

def getPlayer(p_id):
    if p_id == -1:
        return "Empty!"
    else:
        return get_object_or_404(Player, pk= p_id)

@login_required
def createTeam(request):
    player_list = Player.objects.all().filter(user_id=request.user.id)
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
    player_list = Player.objects.all().filter(user_id=request.user.id)
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
            return render_to_response('hockey/contractOfferSuccess.html',{'user':request.user, 'player_list':player_list, 'team_list':team_list})
        else:
            form = OfferPlayerContractForm(request.POST)
            can_manage = False
            owner = False
            if player_list.filter(pk=player_id).count() is 1:
                owner = True
            if len(team_list)>0:
                can_manage = True
                return render_to_response('hockey/offerPlayerContract.html',{'form':form, 'user':request.user, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage,'not_valid':True, 'owner':owner}, context_instance=RequestContext(request))
    else:
        form = OfferPlayerContractForm()
        can_manage = False
        if len(team_list)>0:
            can_manage = True
        return render_to_response('hockey/offerPlayerContract.html',{'form':form, 'user':request.user, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage}, context_instance=RequestContext(request))

@login_required
def messagePlayer(request, player_id):
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    if request.method == 'POST':
        form = MessageForm(request.POST)
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
            return render_to_response('hockey/contractOfferSuccess.html',{'user':request.user, 'player_list':player_list, 'team_list':team_list})
        else:
            form = OfferPlayerContractForm(request.POST)
            can_manage = False
            if len(team_list)>0:
                can_manage = True
                return render_to_response('hockey/offerPlayerContract.html',{'form':form, 'user':request.user, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage,'not_valid':True}, context_instance=RequestContext(request))
    else:
        form = OfferPlayerContractForm(request.POST)
        can_manage = False
        if len(team_list)>0:
            can_manage = True
        return render_to_response('hockey/offerPlayerContract.html',{'form':form, 'user':request.user, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage}, context_instance=RequestContext(request))

@login_required
def editLines(request, team_id):
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    t = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        form_get = make_edit_lines_form(player_list)
        form = form_get(request.POST)
        if form.is_valid():
            t_players = t.players
            cd = form.cleaned_data
            l1 = cd['l1_field']
            c1 = cd['c1_field']
            r1 = cd['r1_field']
            d1 = cd['d1_field']
            g1 = cd['g1_field']
            l2 = cd['l2_field']
            c2 = cd['c2_field']
            r2 = cd['r2_field']
            d2 = cd['d2_field']
            g2 = cd['g2_field']
            l3 = cd['l3_field']
            c3 = cd['c3_field']
            r3 = cd['r3_field']
            d3 = cd['d3_field']
            l4 = cd['l4_field']
            c4 = cd['c4_field']
            r4 = cd['r4_field']
            d4 = cd['d4_field']
            d5 = cd['d5_field']
            d6 = cd['d6_field']
            if player_id_in_team(l1,t_players):
                t.lw1 = l1
                t_players = t_players.exclude(pk = l1)
            if player_id_in_team(l2,t_players):
                t.lw2 = l2
                t_players = t_players.exclude(pk = l2)
            if player_id_in_team(l3,t_players):
                t.lw3 = l3
                t_players = t_players.exclude(pk = l3)
            if player_id_in_team(l4,t_players):
                t.lw4 = l4
                t_players = t_players.exclude(pk = l4)

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

            if player_id_in_team(r1,t_players):
                t.rw1 = r1
                t_players = t_players.exclude(pk = r1)
            if player_id_in_team(r2,t_players):
                t.rw2 = r2
                t_players = t_players.exclude(pk = r2)
            if player_id_in_team(r3,t_players):
                t.rw3 = r3
                t_players = t_players.exclude(pk = r3)
            if player_id_in_team(r4,t_players):
                t.rw4 = r4
                t_players = t_players.exclude(pk = r4)

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
        form = make_edit_lines_form(player_list)
    return render_to_response('hockey/editLines.html',{'form':form, 'user':request.user, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage(request.user.id,t.owner,t.general_Manager)}, context_instance=RequestContext(request))


def can_manage(request_user_id,team_owner, team_general_manager):
    if request_user_id == team_owner or request_user_id == team_general_manager:
        return True
    return False
        
#def check_lines(l1,l2,l3,l4,c1,c2,c3,c4,r1,r2,r3,r4,d1,d2,d3,d4,d5,d6,g1,g2):

def player_id_in_team(p_id,playerlist):
    if playerlist.filter(pk=p_id).count() == 1:
        return True
    return False
