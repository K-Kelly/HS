from wuska.hockey.models import *
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from wuska.hockey.forms import *
from django.db.models import Q


def registration_complete_simple(request,username):
    return redirect('/users/%s/'%(request.user.id))

def index(request):
    if not request.user.is_authenticated():
        return render_to_response('index.html',{},context_instance=RequestContext(request))
    else:
        player_list = request.user.get_profile().players.all()
        team_list = request.user.get_profile().teams.all()
        return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list},context_instance=RequestContext(request))

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
    return render_to_response('profile.html', {'user':request.user,'player_list':player_list, 'team_list':team_list,'owner':owner})

@login_required
def viewMessages(request, player_id):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list})

@login_required
def messagePlayer(request, player_id):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list})

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

    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    return render_to_response('hockey/viewFreeAgents.html',{'user':request.user,'player_list':player_list, 'team_list':team_list, 'FA_list':FA_list, 'position':position, 'have_previous':have_previous,'have_next':have_next,'next_number':next_number,'previous_number':previous_number})

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
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    return render_to_response('hockey/viewAllPlayers.html',{'user':request.user,'player_list':player_list, 'team_list':team_list, 'all_player_list':all_player_list, 'position':position, 'have_previous':have_previous,'have_next':have_next,'next_number':next_number,'previous_number':previous_number})

@login_required
def viewAllTeams(request,number):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    number,have_previous,have_next,previous_number,next_number = pagination_vars(number,25,Team.objects.count())
    all_team_list = Team.objects.order_by('name')[(previous_number):number]
    return render_to_response('hockey/viewAllTeams.html',{'user':request.user,'player_list':player_list, 'team_list':team_list, 'all_team_list':all_team_list, 'have_previous':have_previous,'have_next':have_next,'next_number':next_number,'previous_number':previous_number})

@login_required
def viewAllUsers(request,number):
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all() 
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
    return render_to_response('viewAllUsers.html',{'user':request.user,'player_list':player_list, 'team_list':team_list, 'all_user_list':all_user_list, 'have_previous':have_previous,'have_next':have_next,'next_number':next_number,'previous_number':previous_number})

@login_required
def userViewMessagesRedirect(request, user_id):
    return redirect('/users/%s/viewMessages/received/10/'%(user_id))
@login_required
def userViewMessages(request, user_id, last_message,sent_or_rec):
    profile = request.user.get_profile()
    player_list = profile.players.all()
    team_list = profile.teams.all()
    sent = False
    if sent_or_rec == "sent":
        sent = True
    owner = False
    if request.user.id == int(user_id):
        owner = True
    if owner:
        last_message = int(last_message)
        newer_message = last_message - 10
        older_message = last_message + 10
        have_new_messages = False
        have_older_messages = True
        num_messages = profile.messages.count()
        if older_message >= num_messages:
            have_older_messages = False
        if last_message <10:
            last_message = 10
            newer_message = last_message
        elif last_message > 10:
            have_new_messages = True
        message_list = profile.messages.order_by('-id')[(newer_message):last_message]
        from_list = []
        href_list = []
        name_list = []
        for message in message_list:
            if sent:
                if message.receiver_players.count() == 1:
                    from_list.append("Player: ")
                    player = messages.receiver_players.all()[:1].get()
                    href_list.append("/player/%d/"%(player.id))
                    name_list.append(player.name)
                        
                elif message.receiver_team_id != -1:
                    t = get_object_or_404(Team,pk=message.receiver_team_id)
                    from_list.append("Team: ")
                    href_list.append("/team/%d/"%(t.id))
                    name_list.append(t.name)
                elif message.receiver_user_id != -1 and message.receiver_user_id != user_id:
                    from_list.append("Agent: ")
                    href_list.append("/users/%d/"%(message.receiver_user_id))
                    rec_user = get_object_or_404(User,pk=message.receiver_user_id)
                    name_list.append(rec_user.username) 
            else:
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
                elif message.sender_user_id != -1 and message.sender_user_id != user_id:
                    from_list.append("Agent: ")
                    href_list.append("/users/%d/"%(message.sender_user_id))
                    name_list.append(request.user.username)            
        m_list = zip(message_list,from_list,href_list,name_list)  
        return render_to_response('userViewMessages.html', {'user':request.user,'owner':owner, 'player_list':player_list, 'team_list':team_list,'message_list':m_list,'older_message':older_message,'newer_message':newer_message,'have_new_messages':have_new_messages,'have_older_messages':have_older_messages,'sent':sent},context_instance=RequestContext(request))
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
