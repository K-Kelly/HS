from wuska.hockey.models import *
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from wuska.hockey.forms import *
from django.db.models import Q

def index(request):
    if not request.user.is_authenticated():
        return render_to_response('index.html',{},context_instance=RequestContext(request))
    else:
        player_list = request.user.get_profile().players.all()
        team_list = Team.objects.filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
        return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list},context_instance=RequestContext(request))

@login_required    
def profile(request):
    profile = request.user.get_profile()
    player_list = profile.players.all()
    team_list = Team.objects.filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('profile.html', {'user':request.user,'player_list':player_list, 'team_list':team_list,'profile':profile})

@login_required    
def publicProfile(request,user_id):
    profile = request.user.get_profile()
    player_list = profile.players.all()
    team_list = Team.objects.filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('profile.html', {'user':request.user,'player_list':player_list, 'team_list':team_list,'profile':profile})

def registration_complete_simple(request,username):
    return redirect('/profile/')

@login_required
def viewMessages(request, player_id):
    player_list = request.user.get_profile().players.all()
    team_list = Team.objects.filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list})

@login_required
def messagePlayer(request, player_id):
    player_list = request.user.get_profile().players.all()
    team_list = Team.objects.filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
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
    team_list = Team.objects.filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
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
    team_list = Team.objects.filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('hockey/viewAllPlayers.html',{'user':request.user,'player_list':player_list, 'team_list':team_list, 'all_player_list':all_player_list, 'position':position, 'have_previous':have_previous,'have_next':have_next,'next_number':next_number,'previous_number':previous_number})


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
