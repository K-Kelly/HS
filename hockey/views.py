from hockey.models import *
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from wuska.hockey.forms import *
from django.db.models import Q

def index(request):
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list})

@login_required
def viewPlayer(request, player_id):
    p = get_object_or_404(Player, pk=player_id)
    can_upgrade = False
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    can_manage = False
    if len(team_list)>0:
        can_manage = True
    if p.upgrades >= 1 :
        can_upgrade = True
    if request.user.id == p.user_id:
        return render_to_response('hockey/viewPlayer.html', {'player': p, 'user':request.user, 'can_upgrade':can_upgrade, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage, 'owner':True},context_instance=RequestContext(request))
    else:
        return render_to_response('hockey/viewPlayer.html', {'player':p, 'user':request.user, 'not_owner':True, 'can_upgrade':can_upgrade, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage},context_instance=RequestContext(request))

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
    if request.user.id == t.owner or request.user.id == t.general_Manager:
        return render_to_response('hockey/viewTeam.html', {'team':t, 'user':request.user,'current_lines':current_lines, 'player_list':player_list, 'team_list':team_list, 'can_manage':True, 'offsetf':"span6", 'offsetd':"span6 offset3", 'offsetg':"span6 offset6"}, context_instance=RequestContext(request))
    else:
        return render_to_response('hockey/viewTeam.html', {'team':t, 'user':request.user, 'current_lines':current_lines, 'player_list':player_list,'team_list':team_list, 'can_manage':False, 'offsetf':"span6 offset5", 'offsetd':"span6 offset8", 'offsetg':"span6 offset11"})

def getPlayer(p_id):
    if p_id == -1:
        return "Empty!"
    else:
        return get_object_or_404(Player, pk= p_id).name

@login_required    
def profile(request):
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('profile.html', {'user':request.user,'player_list':player_list, 'team_list':team_list,'profile':request.user.get_profile()})

@login_required
def createPlayer(request):
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('hockey/createPlayer.html', {'user':request.user, 'player_list':player_list, 'team_list':team_list},context_instance=RequestContext(request))

@login_required
def upgradeSkill(request, player_id):
    if request.method == 'POST':
        p = get_object_or_404(Player, pk=player_id)
        skill = request.POST['skill']
        if request.user.id == p.user_id and p.upgrades > 0:
             doUpgradeSkill(skill,p)
             return redirect('/player/%s' %(player_id))
        else:
            return render_to_response('hockey/no_upgrades.html',)
    else:
        return render_to_response('hockey/no_upgrades.html',)  

@login_required
def creatingPlayer(request):
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    if request.method == 'POST' and 'name' in request.POST and request.POST['name']!="" and 'position' in request.POST and request.POST['position'] and 'height' in request.POST and request.POST['height'] and 'weight' in request.POST and request.POST['weight']:
        name = request.POST['name']
        position = request.POST['position']
        height = request.POST['height']
        weight = request.POST['weight']  
        team_id = -1 #free agent
        user_id = request.user.id 
        upgrades = 10
        level = 1
        experience = 0
        age = 18
        retired = False
        salary = 0
        contract_end = 0
        no_trade = False
        style = 1 # need to make user choose this
        shooting = 1
        passing = 1
        stickHandling = 1
        checking = 1
        positioning = 1
        endurance = 1
        skating = 1
        strength = 1
        faceoff = 1
        fighting = 1
        awareness = 1
        leadership = 1
        helmet = 0
        gloves = 0
        shoulder_pads = 0
        pants = 0
        skates = 0
        stick = 0
        player = Player(team_id = team_id, user_id = user_id, upgrades = upgrades, level = level, experience = experience, name = name, age = age, retired = retired, height = height, weight = weight, salary =salary, contract_end = contract_end, no_trade = no_trade, position = position, style = style, shooting = shooting, passing = passing, stickHandling = stickHandling, checking = checking, positioning = positioning, endurance = endurance, skating = skating, strength = strength, faceoff = faceoff, fighting = fighting, awareness = awareness, leadership = leadership, helmet = helmet, gloves = gloves, shoulder_pads = shoulder_pads, pants = pants, skates = skates, stick = stick)
        player.save()
        request.user.get_profile().players.add(player)        
        return render_to_response('hockey/createPlayerSuccess.html',{'user':request.user, 'player_list':player_list, 'team_list':team_list})
    else:
        return render_to_response('hockey/createPlayer.html', {'error': True, 'user':request.user, 'player_list':player_list, 'team_list':team_list}, context_instance=RequestContext(request))


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
            return render_to_response('hockey/createTeamSuccess.html',{'user':request.user, 'player_list':player_list, 'team_list':team_list})
    else:
        form = TeamForm()
    return render_to_response('hockey/createTeam.html',{'form':form, 'user':request.user, 'player_list':player_list, 'team_list':team_list}, context_instance=RequestContext(request))

def doUpgradeSkill(skill,player):
    if player.upgrades >0:
        if skill == "shooting":
            player.shooting +=1
        elif skill == "passing":
            player.passing +=1
        elif skill == "stickHandling":
            player.stickHandling +=1
        elif skill == "checking":
            player.checking += 1
        elif skill == "positioning":
            player.positioning +=1
        elif skill == "endurance":
            player.endurance +=1
        elif skill == "skating":
            player.skating +=1
        elif skill == "strength":
            player.strength +=1
        elif skill == "faceoff":
            player.faceoff +=1
        elif skill == "awareness":
            player.awareness +=1
        elif skill == "leadership":
            player.leadership +=1
        elif skill == "fighting":
            player.fighting +=1
        else:
            player.upgrades +=1
        player.upgrades -=1
        player.save()

@login_required        
def viewContracts(request, player_id):
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    
    player = get_object_or_404(Player, pk=player_id)
    owner = False
    if player.user_id == request.user.id:
        owner = True
    contract_list = player.contracts.all() 
    if request.method == 'POST':
        if 'Reject' in request.POST:
            contract_id = request.POST['Reject']
            Contract.objects.get(pk=contract_id).delete()
        elif 'Accept' in request.POST:
            contract_id = request.POST['Accept']
            contract = get_object_or_404(Contract, pk=contract_id)
            team = get_object_or_404(Team,pk=contract.team_id)
            team.players.add(player)
            team.contracts.remove(contract)
            team.salary_used += contract.salary
            team.salary_left -= contract.salary
            team.save()
            player.salary=contract.salary
            player.team_id = contract.team_id
            player.contracts.clear()
            player.contract_end = contract.length
            player.no_trade = contract.no_trade
            player.save()
            Contract.objects.get(pk=contract_id).delete()
        return redirect('/player/%s' %(player_id))
            
    return render_to_response('hockey/viewContractOffersPlayer.html',{'user':request.user,'player_list':player_list, 'team_list':team_list, 'contract_list':contract_list, 'owner':owner},context_instance=RequestContext(request))

@login_required
def viewMessages(request, player_id):
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list})

@login_required
def buyEquipment(request, player_id):
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list})

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
def messagePlayer(request, player_id):
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list})

