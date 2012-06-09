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
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    can_upgrade = False
    if p.upgrades > 0 :
        can_upgrade = True
    owner = False
    if request.user.id == p.user_id:
        owner = True
    return render_to_response('hockey/viewPlayer.html', {'player': p, 'user':request.user, 'can_upgrade':can_upgrade, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage_by_num_teams(team_list), 'owner':owner, 'not_owner':not(owner), 'alert_success':""},context_instance=RequestContext(request))


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
        free_agent = True
        player = Player(team_id = team_id, user_id = user_id, upgrades = upgrades, level = level, experience = experience, name = name, age = age, retired = retired, height = height, weight = weight, salary =salary, contract_end = contract_end, no_trade = no_trade, position = position, style = style, shooting = shooting, passing = passing, stickHandling = stickHandling, checking = checking, positioning = positioning, endurance = endurance, skating = skating, strength = strength, faceoff = faceoff, fighting = fighting, awareness = awareness, leadership = leadership, helmet = helmet, gloves = gloves, shoulder_pads = shoulder_pads, pants = pants, skates = skates, stick = stick, free_agent = free_agent)
        player.save()
        request.user.get_profile().players.add(player) 
        next = "/player/%s"%(player.pk)
        return redirect(next)
        #return render_to_response('hockey/createPlayerSuccess.html',{'user':request.user, 'player_list':player_list, 'team_list':team_list})
    else:
        return render_to_response('hockey/createPlayer.html', {'error': True, 'user':request.user, 'player_list':player_list, 'team_list':team_list}, context_instance=RequestContext(request))

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
            player.free_agent = False
            player.save()
            Contract.objects.get(pk=contract_id).delete()
        return redirect('/player/%s' %(player_id))
            
    return render_to_response('hockey/viewContractOffersPlayer.html',{'user':request.user,'player':player,'player_list':player_list, 'team_list':team_list, 'contract_list':contract_list, 'owner':owner},context_instance=RequestContext(request))

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
def messagePlayer(request, player_id):
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    player = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        form_get = message_player(team_list)
        form = form_get(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            title = cd['title']
            body = cd['body']
            team_field = cd['team_field']
            message = Message(sender_user_id=request.user.id,sender_player_id=-1,sender_team_id=team_field,receiver_team_id=-1,title=title,body=body)
            message.save()
            message.receiver_players.add(player)
            message.save()
            player.messages.add(message)
            player.save()
            can_upgrade = False
            if player.upgrades > 0 :
                can_upgrade = True
            owner = False
            if player.id == request.user.id:
                owner = True
            alert="Message sent to %s." %(player.name)
            return render_to_response('hockey/viewPlayer.html', {'player':player, 'user':request.user,'owner':owner, 'not_owner':not(owner), 'can_upgrade':can_upgrade, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage_by_num_teams(team_list),'alert_success':True,'alert_message':alert},context_instance=RequestContext(request))
    else:
        form = message_player(team_list)
    return render_to_response('hockey/messagePlayer.html',{'form':form, 'user':request.user, 'player':player,'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage_by_num_teams(team_list)}, context_instance=RequestContext(request))




def can_manage(request_user_id,team_owner, team_general_manager):
    if request_user_id == team_owner or request_user_id == team_general_manager:
        return True
    return False 

def can_manage_by_num_teams(team_list):
    if team_list.count >0:
        return True
    return False
