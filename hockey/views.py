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
    return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list},context_instance=RequestContext(request))

@login_required    
def profile(request):
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('profile.html', {'user':request.user,'player_list':player_list, 'team_list':team_list,'profile':request.user.get_profile()})

@login_required
def viewMessages(request, player_id):
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list})

@login_required
def messagePlayer(request, player_id):
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list})

@login_required
def messageTeam(request, team_id):
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list})

@login_required
def viewFreeAgents(request, position):
    if position == "L" or position == "C" or position == "R" or position == "D" or position == "G":
        FA_list = Player.objects.all().filter(position = position,free_agent=True).order_by('-level','name')
    else:
        FA_list = Player.objects.all().filter(free_agent=True).order_by('-level','name')
    player_list = Player.objects.all().filter(user_id=request.user.id)
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('hockey/viewFreeAgents.html',{'user':request.user,'player_list':player_list, 'team_list':team_list, 'FA_list':FA_list, 'position':position})
