from wuska.hockey.models import *
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from wuska.league.forms import *
from django.db.models import Q
from django.contrib.auth.models import User
from wuska.accounts.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from random import randrange

@login_required
def viewLeague(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    division1 = league.division1.all()
    division2 = league.division2.all()
    division3 = league.division3.all()
    division4 = league.division4.all()
    division5 = league.division5.all()
    division6 = league.division6.all()
    return render_to_response('league/viewLeague.html', {'league':league, 'user':request.user,'profile':request.user.get_profile(),'player_list':player_list, 'team_list':team_list,'division1':division1,'division2':division2,'division3':division3,'division4':division4,'division5':division5,'division6':division6}, context_instance=RequestContext(request))

@login_required
def scheduleNewSeason(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ScheduleNewSeasonForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                start_datetime = cd['start_datetime']
                league_list = League.objects.all()
                season_length = 70
                season_number = 1 ###Increment for each new season
                #season will last for 70 days
                #4 games (2 home, 2 away) against divisional teams
                #2 games (1 home, 1 away) against teams within conference
                #divison1,2,3 = conference1, divison4,5,6 = conference2
                #1 game against teams outside of conference.
                #if 10 teams out of conference then 5 home, 5 away
                for league in league_list:
                    div1 = league.division1.all()
                    div2 = league.division2.all()
                    div3 = league.division3.all()
                    div4 = league.division4.all()
                    div5 = league.division5.all()
                    div6 = league.division6.all()
                    for team in league.teams.all():
                        team_season=TeamSeason(team_id=team.id,league_id=league.id,season_number=season_number)
                        team_season.save()
                        league.standings.add(team_season)
                        league.save()
                        team.seasons.add(team_season)
                        team.save()
                    for team in div1:
                        team_season1 = team.seasons.filter(season_number=season_number)
                        for team2 in div1:
                            team_season2 = team2.seasons.filter(season_number=season_number)
                            game1h =        

        else:
            form = ScheduleNewSeasonForm()
        return render_to_response('league/scheduleNewSeason.html',{'user':request.user,'profile':request.user.get_profile(),'player_list':request.user.get_profile().players.all(),'team_list':request.user.get_profile().teams.all()},context_instance=RequestContext(request))
                
    else:
        return render_to_response('404.html',{'user':request.user,'profile':request.user.get_profile(),'player_list':request.user.get_profile().players.all(),'team_list':request.user.get_profile().teams.all()},context_instance=RequestContext(request))


#@is_home : if team_season1's team is the home team for this game
def find_valid_date(team_season1,team_season2,season_length,start_datetime,is_home):
    #calculate the day of a game
    daytime = start_datetime + datetime.timedelta(randrange(0,season_length))
    check_team1 = check_valid_day_team(team_season1,daytime)
    check_team2 = check_valid_day_team(team_season2,daytime)
    while (not(check_team1) or not(check_team2)):
        daytime = start_datetime + datetime.timedelta(randrange(0,season_length))
        check_team1 = check_valid_day_team(team_season1,daytime)
        check_team2 = check_valid_day_team(team_season2,daytime)
    game_datetime = datetime(daytime.year,daytime.month,daytime.day,randrange(11,22),10*randrange(0,6))
    if is_home:
        game = Game(home_team=team_season1.team.id,away_team=team_season2.team.id,is_playoff=False,game_datetime,has_started=False,is_completed=False)
        game.save()
        team_season1.reg_games.add(game)
        team_season1.save()
        team_season2.reg_games.add(game)
        team_season2.save()
    else:
        game = Game(home_team=team_season2.team.id,away_team=team_season1.team.id,is_playoff=False,game_datetime,has_started=False,is_completed=False)
        game.save()
        team_season1.reg_games.add(game)
        team_season1.save()
        team_season2.reg_games.add(game)
        team_season2.save()

def check_valid_day_team(team_season,check_datetime):
    for game in team_season.reg_games.all():
            if check_datetime.date() == game.datetime.date():
                return False
    return True
    
