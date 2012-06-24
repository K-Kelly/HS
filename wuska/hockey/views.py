from wuska.hockey.models import *
from wuska.hockey.forms import *
from wuska.accounts.models import UserProfile
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def registration_complete_simple(request,username):
    return redirect('/users/%s/'%(request.user.id))

def index(request):
    if not request.user.is_authenticated():
        return render_to_response('index.html',{},context_instance=RequestContext(request))
    else:
        player_list = request.user.get_profile().players.all()
        team_list = request.user.get_profile().teams.all()
        return render_to_response('index.html',{'user':request.user,'profile':request.user.get_profile(),'player_list':player_list, 'team_list':team_list},context_instance=RequestContext(request))

@login_required
def profileRedirect(request):
    return redirect("/users/%s/"%(request.user.id))

@login_required    
def profile(request,user_id):
    profile = request.user.get_profile()
    player_list = profile.players.all()
    team_list = profile.teams.all()
    owner = False
    if request.user.id == int(user_id):
        owner = True
    return render_to_response('profile.html', {'user':request.user,'profile':profile,'player_list':player_list, 'team_list':team_list,'owner':owner,'profile':profile})

@login_required
def viewFreeAgentsRedirect(request):
    return redirect("/freeAgents/All/25/")
def viewFreeAgentsRedirect2(request,position):
    return redirect("/freeAgents/%s/25/"%(position))
@login_required
def viewFreeAgents(request, position, number):
    if position == "L" or position == "C" or position == "R" or position == "D" or position == "G":
        FA_list = Player.objects.filter(position = position,free_agent=True).order_by('-level','name')
        number,have_previous,have_next,previous_number,next_number = pagination_vars(number,25,Player.objects.filter(position=position,free_agent=True).count())
    else:
        FA_list = Player.objects.filter(free_agent=True).order_by('-level','name')
        number,have_previous,have_next,previous_number,next_number = pagination_vars(number,25,Player.objects.filter(position=position,free_agent=True).count())
    
    profile = request.user.get_profile()
    player_list = profile.players.all()
    team_list = profile.teams.all()
    return render_to_response('hockey/viewFreeAgents.html',{'user':request.user,'profile':profile,'player_list':player_list, 'team_list':team_list, 'FA_list':FA_list, 'position':position, 'have_previous':have_previous,'have_next':have_next,'next_number':next_number,'previous_number':previous_number})

@login_required
def viewAllPlayersRedirect(request):
    return redirect("/allPlayers/All/25/")
@login_required
def viewAllPlayersRedirect2(request,position):
    return redirect("/allPlayers/%s/25/"%(position))
@login_required
def viewAllPlayers(request, position, number):
    number,have_previous,have_next,previous_number,next_number = pagination_vars(number,25,Player.objects.count())

    if position == "L" or position == "C" or position == "R" or position == "D" or position == "G":
        all_player_list = Player.objects.filter(position = position).order_by('-level','name')[(previous_number):number]
    else:
        all_player_list = Player.objects.order_by('-level','name')[(previous_number):number]
    profile = request.user.get_profile()
    player_list = profile.players.all()
    team_list = profile.teams.all()
    return render_to_response('hockey/viewAllPlayers.html',{'user':request.user,'profile':profile,'player_list':player_list, 'team_list':team_list, 'all_player_list':all_player_list, 'position':position, 'have_previous':have_previous,'have_next':have_next,'next_number':next_number,'previous_number':previous_number})

@login_required
def viewAllTeams(request,number):
    profile = request.user.get_profile()
    player_list = profile.players.all()
    team_list = profile.teams.all()
    number,have_previous,have_next,previous_number,next_number = pagination_vars(number,25,Team.objects.count())
    all_team_list = Team.objects.order_by('name')[(previous_number):number]
    return render_to_response('hockey/viewAllTeams.html',{'user':request.user,'profile':profile,'player_list':player_list, 'team_list':team_list, 'all_team_list':all_team_list, 'have_previous':have_previous,'have_next':have_next,'next_number':next_number,'previous_number':previous_number})

@login_required
def viewAllUsers(request,number):
    profile = request.user.get_profile()
    player_list = profile.players.all()
    team_list = profile.teams.all()
    number,have_previous,have_next,previous_number,next_number = pagination_vars(number,25,User.objects.count())
    user_list = User.objects.order_by('username')[(previous_number):number]
    name_list = []
    player_list_all = []
    teams_owned = []
    teams_gmed = []
    for user in user_list:
        profile = user.get_profile()
        name_list.append(user.username)
        player_list_all.append(profile.players.all())
        teams_owned.append(profile.teams_owned.all())
        teams_gmed.append(profile.teams_gmed.all())
    all_user_list = zip(name_list,player_list_all,teams_owned,teams_gmed)
    return render_to_response('viewAllUsers.html',{'user':request.user,'profile':profile,'player_list':player_list, 'team_list':team_list, 'all_user_list':all_user_list, 'have_previous':have_previous,'have_next':have_next,'next_number':next_number,'previous_number':previous_number})

@login_required
def userViewMessagesRedirect(request, user_id):
    return redirect('/users/%s/viewMessages/received/10/'%(user_id))
@login_required
def userViewMessages(request, user_id, last_message,sent_or_rec):
    profile = request.user.get_profile()
    player_list = profile.players.all()
    team_list = profile.teams.all()
    sent = True if sent_or_rec == "sent" else False
    owner = True if request.user.id == int(user_id) else False
    if owner:
        profile.new_message = False
        profile.save()
        last_message = int(last_message)
        newer_message = last_message - 10
        older_message = last_message + 10
        have_new_messages = False
        have_older_messages = False

        sender_user_list = []
        has_sender_player_list = []
        sender_player_list = []
        has_sender_team_list = []
        sender_team_list = []
        has_sender_cc_list = []
        sender_cc_list = []
        has_concerning_players_list = []
        concerning_players_list = []
        has_concerning_teams_list = []
        concerning_teams_list = []
        receiver_users_list = []
        is_automated_list = []
        if sent:
            message_list = profile.messages.filter(sender_user_id = profile.id).order_by('-id')[(newer_message):last_message]
            num_messages = profilemessages.filter(sender_user_id = profile.id).count()
        else:
            message_list = profile.messages.filter(receiver_users__id__exact=profile.id).order_by('-id')[(newer_message):last_message]
            num_messages = profile.messages.filter(receiver_users__id__exact=profile.id).order_by('-id').count()

        if last_message <10:
            last_message = 10
            newer_message = last_message
        elif last_message > 10:
            have_new_messages = True
        if num_messages > last_message:
            have_older_messages = True

        for message in message_list:  
            sender_user_list.append(get_object_or_404(UserProfile,pk=message.sender_user_id))
            has_sender_cc_list.append(True if message.sender_cc_users.count()>0 else False)
            sender_cc_list.append(message.sender_cc_users.all())
            has_concerning_players_list.append(True if message.concerning_players.count()>0 else False)
            concerning_players_list.append(message.concerning_players.all())
            has_concerning_teams_list.append(True if message.concerning_teams.count()>0 else False)
            concerning_teams_list.append(message.concerning_teams.all())
            receiver_users_list.append(message.receiver_users.all())
            is_automated_list.append(message.is_automated)
            if message.sender_player_id == -1:
                has_sender_player_list.append(False)
                sender_player_list.append(None)
            else:
                has_sender_player_list.append(True)
                sender_player_list.append(get_object_or_404(Player,pk=message.sender_player_id))
            if message.sender_team_id == -1:
                has_sender_team_list.append(False)
                sender_team_list.append(None)
            else:
                has_sender_team_list.append(True)
                sender_team_list.append(get_object_or_404(Team,pk=message.sender_team_id))                      
        m_list = zip(message_list,sender_user_list,has_sender_player_list,sender_player_list,has_sender_team_list,sender_team_list,has_sender_cc_list,sender_cc_list,has_concerning_players_list,concerning_players_list,has_concerning_teams_list,concerning_teams_list,receiver_users_list,is_automated_list)

        return render_to_response('userViewMessages.html', {'user':request.user,'profile':profile,'owner':owner, 'player_list':player_list, 'team_list':team_list,'message_list':m_list,'older_message':older_message,'newer_message':newer_message,'have_new_messages':have_new_messages,'have_older_messages':have_older_messages,'sent':sent,'profile':profile},context_instance=RequestContext(request))
    return redirect('/users/%s/'%(user_id))  #user is attempting to access other user's messages


#Sets up the variables needed for pagination
def pagination_vars(number,per_page,max_number):
    number = int(number)
    have_previous = False
    have_next = True
    next_number = number + per_page
    previous_number = number - per_page
    if number > per_page:
        have_previous = True
    elif number > max_number:
        have_next = False
        number = max_number
    elif number < 0:
        number = 0
    return number,have_previous,have_next,previous_number,next_number

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
