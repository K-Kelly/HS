from wuska.hockey.models import *
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from wuska.hockey.forms import *
from django.db.models import Q

def index(request):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list})

@login_required
def viewPlayer(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    can_upgrade = False
    if player.upgrades > 0 :
        can_upgrade = True
    owner = True if request.user.id == player.user_id else False

    return render_to_response('hockey/viewPlayer.html', {'player': player, 'user':request.user, 'can_upgrade':can_upgrade, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage_by_num_teams(team_list), 'show_manage':True, 'owner':owner, 'not_owner':not(owner),'new_message':player.new_message, 'new_contract':player.new_contract},context_instance=RequestContext(request))


@login_required
def createPlayer(request):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
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
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
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
        stick_handling = 1
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
        player = Player(team_id = team_id, user_id = user_id, upgrades = upgrades, level = level, experience = experience, name = name, age = age, retired = retired, height = height, weight = weight, salary =salary, contract_end = contract_end, no_trade = no_trade, position = position, style = style, shooting = shooting, passing = passing, stick_handling = stick_handling, checking = checking, positioning = positioning, endurance = endurance, skating = skating, strength = strength, faceoff = faceoff, fighting = fighting, awareness = awareness, leadership = leadership, helmet = helmet, gloves = gloves, shoulder_pads = shoulder_pads, pants = pants, skates = skates, stick = stick, free_agent = free_agent,new_message=False,new_contract=False)
        player.save()
        request.user.get_profile().players.add(player) 
        next = "/player/%s"%(player.pk)
        return redirect(next)
    else:
        return render_to_response('hockey/createPlayer.html', {'error': True, 'user':request.user, 'player_list':player_list, 'team_list':team_list}, context_instance=RequestContext(request))

def doUpgradeSkill(skill,player):
    if player.upgrades >0:
        if skill == "shooting":
            player.shooting +=1
        elif skill == "passing":
            player.passing +=1
        elif skill == "stick_handling":
            player.stick_handling +=1
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
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all() 
    player = get_object_or_404(Player, pk=player_id)
    owner = False   
    if player.user_id == request.user.id:
        owner = True
        player.new_contract = False #owner is viewing contracts
        player.save()
    contract_list = player.contracts.all() 
    if request.method == 'POST' and owner:
        if 'Reject' in request.POST:
            contract_id = request.POST['Reject']
            contract = get_object_or_404(Contract,pk=contract_id)
            team = get_object_or_404(Team,pk=contract.team_id)
            team.contract_status_change = True
            team.save()
            if contract.player_id == player_id:
                contract.delete()
        elif 'Accept' in request.POST:
            contract_id = request.POST['Accept']
            contract = get_object_or_404(Contract,pk=contract_id)
            if contract not in player.contracts.all():
                return redirect('/player/%s/viewContracts' %(player_id))
            team = get_object_or_404(Team,pk=contract.team_id)
            team.salary_used += contract.salary
            team.salary_left -= contract.salary
            if player.position == "L":
                team.numLWNeed -= 1
            elif player.position == "C":
                team.numCNeed -= 1
            elif player.position == "R":
                team.numRWNeed -= 1
            elif player.position == "D":
                team.numDNeed -= 1
            elif player.position == "G":
                team.numGNeed -= 1
            else:
                return redirect('/player/%s/viewContracts' %(player_id))   

            team_age_sum = team.avgAge * team.players.count()
            team_age_sum += player.age
            team.players.add(player)
            team.avgAge = team_age_sum / team.players.count() 
            team.contract_status_change = True
            team.save()
            player.salary=contract.salary
            player.team_id = contract.team_id
            player.contracts.clear()
            player.contract_end = contract.length
            player.no_trade = contract.no_trade
            player.free_agent = False
            player.save()
            contract.is_accepted = True
            contract.save()
            return redirect('/player/%s' %(player_id))          
    return render_to_response('hockey/viewContractOffersPlayer.html',{'user':request.user,'player':player,'player_list':player_list, 'team_list':team_list, 'contract_list':contract_list, 'owner':owner,'can_manage':can_manage_by_num_teams(team_list),'show_manage':False,'new_message':player.new_message, 'new_contract':player.new_contract},context_instance=RequestContext(request))

@login_required
def viewMessagesRedirect(request, player_id):
    return redirect('/player/%s/viewMessages/received/10'%(player_id))
@login_required
def viewMessages(request, player_id, last_message,sent_or_rec):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    player = get_object_or_404(Player, pk=player_id)
    sent = False
    #if sent_or_rec == "sent":#Players don't currently "send" messages, so shouldn't show "Go To Sent Button"
    #    sent = True
    if request.user.id == player.user_id:
        if player.new_message:
            player.new_message = False
            player.save()
        last_message = int(last_message)
        newer_message = last_message - 10
        older_message = last_message + 10
        have_new_messages = False
        have_older_messages = True
        num_messages = player.messages.count()
        if older_message >= num_messages:
            have_older_messages = False
        if last_message <10:
            last_message = 10
            newer_message = last_message
        elif last_message > 10:
            have_new_messages = True
        message_list = player.messages.order_by('-id')[(newer_message):last_message]
        from_list = []
        href_list = []
        name_list = []
        for message in message_list:
            if message.sender_player_id != -1:
                p = get_object_or_404(Player,pk=message.sender_player_id)
                from_list.append("Player: ")
                href_list.append("/player/%d/"%(p.id))
                name_list.append(p.name)
            elif message.sender_team_id != -1:
                t = get_object_or_404(Team,pk=message.sender_team_id)
                from_list.append("Team: ")
                href_list.append("/team/%d/"%(t.id))
                name_list.append(t.name)
            else:
                from_list.append("Agent: ")
                href_list.append("/users/%d/"%(message.sender_user_id))
                name_list.append(request.user.username)            
        m_list = zip(message_list,from_list,href_list,name_list)  
        return render_to_response('hockey/playerViewMessages.html', {'player': player, 'user':request.user, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage_by_num_teams(team_list), 'show_manage':False,'message_list':m_list,'older_message':older_message,'newer_message':newer_message,'have_new_messages':have_new_messages,'have_older_messages':have_older_messages,'sent':sent,'owner':True, 'not_owner':False,'new_message':player.new_message, 'new_contract':player.new_contract},context_instance=RequestContext(request))
    return redirect('player/%s/'%(player_id))  #not owner of player

@login_required
def buyEquipment(request, player_id):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list})

@login_required
def messagePlayer(request, player_id):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    player = get_object_or_404(Player, pk=player_id)
    owner = True if player.user_id == request.user.id else False
    if request.method == 'POST':
        form_get = message_player(team_list)
        form = form_get(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            title = cd['title']
            body = cd['body']
            team_field = cd['team_field']
            message = Message(sender_user_id=request.user.id,sender_player_id=-1,sender_team_id=team_field,receiver_team_id=-1,receiver_user_id = player.user_id,title=title,body=body)
            message.save()
            message.receiver_players.add(player)
            message.save()
            player.messages.add(message)
            player.new_message = True
            player.save()
            can_upgrade = False
            if player.upgrades > 0 :
                can_upgrade = True
            alert="Message sent to %s." %(player.name)
            return render_to_response('hockey/viewPlayer.html', {'player':player, 'user':request.user,'owner':owner, 'not_owner':not(owner), 'can_upgrade':can_upgrade, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage_by_num_teams(team_list),'show_manage':True, 'alert_success':True,'alert_message':alert, 'new_message':player.new_message, 'new_contract':player.new_contract},context_instance=RequestContext(request))
        else:
            form = message_player(team_list)
            form = form(request.POST)
            return render_to_response('hockey/messagePlayer.html',{'form':form, 'user':request.user, 'player':player,'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage_by_num_teams(team_list),'show_manage':True,'new_message':player.new_message, 'new_contract':player.new_contract,'owner':owner}, context_instance=RequestContext(request))
    else:
        form = message_player(team_list)
        return render_to_response('hockey/messagePlayer.html',{'form':form, 'user':request.user, 'player':player,'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage_by_num_teams(team_list),'show_manage':True,'new_message':player.new_message, 'new_contract':player.new_contract,'owner':owner}, context_instance=RequestContext(request))



def can_manage(request_user_id,team_owner, team_general_manager1, team_general_manager2):
    if request_user_id == team_owner or request_user_id == team_general_manager1 or request_user_id == team_general_manager2:
        return True
    return False 

# a user is a team manager if the number of teams in their profile is > 0
def can_manage_by_num_teams(team_list):
    if team_list.count() >0:
        return True
    return False
