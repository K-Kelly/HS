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
        team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
        return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list},context_instance=RequestContext(request))

@login_required    
def profile(request):
    profile = request.user.get_profile()
    player_list = profile.players.all()
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('profile.html', {'user':request.user,'player_list':player_list, 'team_list':team_list,'profile':profile})

@login_required    
def publicProfile(request,user_id):
    profile = request.user.get_profile()
    player_list = profile.players.all()
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('profile.html', {'user':request.user,'player_list':player_list, 'team_list':team_list,'profile':profile})

def registration_complete_simple(request,username):
    return redirect('/profile/')

@login_required
def viewMessages(request, player_id):
    player_list = request.user.get_profile().players.all()
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list})

@login_required
def messagePlayer(request, player_id):
    player_list = request.user.get_profile().players.all()
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('index.html',{'user':request.user,'player_list':player_list, 'team_list':team_list})

@login_required
def viewFreeAgents(request, position):
    if position == "L" or position == "C" or position == "R" or position == "D" or position == "G":
        FA_list = Player.objects.all().filter(position = position,free_agent=True).order_by('-level','name')
    else:
        FA_list = Player.objects.all().filter(free_agent=True).order_by('-level','name')
    player_list = request.user.get_profile().players.all()
    team_list = Team.objects.all().filter(Q(owner=request.user.id)|Q(general_Manager=request.user.id))
    return render_to_response('hockey/viewFreeAgents.html',{'user':request.user,'player_list':player_list, 'team_list':team_list, 'FA_list':FA_list, 'position':position})
