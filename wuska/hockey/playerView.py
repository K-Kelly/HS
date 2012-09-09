from wuska.hockey.models import *
from wuska.hockey.forms import *
from wuska.accounts.models import UserProfile
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

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
    player_owner = get_object_or_404(UserProfile,pk=player.user_id)
    team = get_object_or_404(Team,pk=player.team_id)
    league = get_object_or_404(League,pk=team.league_id)
    return render_to_response('hockey/viewPlayer.html', {'player': player, 'user':request.user, 'profile':request.user.get_profile(),'can_upgrade':can_upgrade, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage_by_num_teams(team_list), 'show_manage':True, 'owner':owner, 'not_owner':not(owner), 'new_contract':player.new_contract,'player_owner':player_owner,'team':team,'league':league},context_instance=RequestContext(request))

@login_required
def createPlayer(request):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    if request.method == 'POST':
        form = CreatePlayerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            position = cd['position']
            height = cd['height']
            weight = cd['weight']
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
            player = Player(team_id = team_id, user_id = user_id, upgrades = upgrades, level = level, experience = experience, name = name, age = age, retired = retired, height = height, weight = weight, salary =salary, contract_end = contract_end, no_trade = no_trade, position = position, style = style, shooting = shooting, passing = passing, stick_handling = stick_handling, checking = checking, positioning = positioning, endurance = endurance, skating = skating, strength = strength, faceoff = faceoff, fighting = fighting, awareness = awareness, leadership = leadership, helmet = helmet, gloves = gloves, shoulder_pads = shoulder_pads, pants = pants, skates = skates, stick = stick, free_agent = free_agent,new_contract=False)
            player.save()
            request.user.get_profile().players.add(player) 
            request.user.get_profile().save()
            next = "/player/%s/"%(player.pk)
            return redirect(next)
        else:
            form = CreatePlayerForm(request.POST)
    else:
        form = CreatePlayerForm()
    return render_to_response('hockey/createPlayer.html', {'user':request.user, 'profile':request.user.get_profile(),'form':form,'player_list':player_list, 'team_list':team_list},context_instance=RequestContext(request))

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
            #inform offering team of contract rejection
            title = "Contract Offer Rejected"
            body = "Player %s has rejected your contract offer of %s for %s season(s)" % (player.name,contract.salary,contract.length)
            receiver_users = [get_object_or_404(UserProfile,pk=team.owner)]
            if team.general_manager1 != -1:
                receiver_users.append(get_object_or_404(UserProfile,pk=team.general_manager1))
            if team.general_manager2 != -1:
                receiver_users.append(get_object_or_404(UserProfile,pk=team.general_manager2))

            send_message(title,body,player.user_id,[],player.id,-1,[],[team],receiver_users,True)
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
            #inform offering team of contract acceptance
            title = "Contract Offer Accepted!"
            body = "Player %s has accepted your contract offer of %s for %s season(s)!" % (player.name,contract.salary,contract.length)
            receiver_users = [get_object_or_404(UserProfile,pk=team.owner)]
            if team.general_manager1 != -1:
                receiver_users.append(get_object_or_404(UserProfile,pk=team.general_manager1))
            if team.general_manager2 != -1:
                receiver_users.append(get_object_or_404(UserProfile,pk=team.general_manager2))

            send_message(title,body,player.user_id,[],player.id,-1,[],[team],receiver_users,True)
            return redirect('/player/%s' %(player_id))          
    return render_to_response('hockey/viewContractOffersPlayer.html',{'user':request.user,'profile':request.user.get_profile(),'player':player,'player_list':player_list, 'team_list':team_list, 'contract_list':contract_list, 'owner':owner,'can_manage':can_manage_by_num_teams(team_list),'show_manage':True, 'new_contract':player.new_contract},context_instance=RequestContext(request))

@login_required
def buyEquipment(request, player_id):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    return render_to_response('index.html',{'user':request.user,'profile':request.user.get_profile(),'player_list':player_list, 'team_list':team_list})

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
            sender_cc_users = []
            if int(team_field) != -1:
                team = get_object_or_404(Team,pk=int(team_field))
                sender_cc_users.append(get_object_or_404(UserProfile,pk=team.owner))
                if team.general_manager1 != -1:
                    sender_cc_users.append(get_object_or_404(UserProfile,pk=team.general_manager1))
                if team.general_manager2 != -1:
                    sender_cc_users.append(get_object_or_404(UserProfile,pk=team.general_manager2))

            send_message(title,body,request.user.id,sender_cc_users,-1,team_field,[player],[],[get_object_or_404(UserProfile,pk=player.user_id)],False)
            can_upgrade = False
            if player.upgrades > 0:
                can_upgrade = True
            alert="Message sent to %s." %(player.name)
            return render_to_response('hockey/viewPlayer.html', {'player':player, 'user':request.user,'profile':request.user.get_profile(),'owner':owner, 'not_owner':not(owner), 'can_upgrade':can_upgrade, 'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage_by_num_teams(team_list),'show_manage':True, 'alert_success':True,'alert_message':alert, 'new_contract':player.new_contract},context_instance=RequestContext(request))
        else:
            form = message_player(team_list)
            form = form(request.POST)
    else:
        form = message_player(team_list)
    return render_to_response('hockey/messagePlayer.html',{'form':form, 'user':request.user, 'profile':request.user.get_profile(),'player':player,'player_list':player_list, 'team_list':team_list, 'can_manage':can_manage_by_num_teams(team_list),'show_manage':True,'new_contract':player.new_contract,'owner':owner}, context_instance=RequestContext(request))



def can_manage(request_user_id,team_owner, team_general_manager1, team_general_manager2):
    if request_user_id == team_owner or request_user_id == team_general_manager1 or request_user_id == team_general_manager2:
        return True
    return False 

# a user is a team manager if the number of teams in their profile is > 0
def can_manage_by_num_teams(team_list):
    if team_list.count() > 0:
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
