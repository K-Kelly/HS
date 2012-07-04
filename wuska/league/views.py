from wuska.hockey.models import *
from wuska.accounts.models import UserProfile
from wuska.league.forms import *
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http500
from random import randrange
from datetime import datetime,timedelta
from itertools import chain

@login_required
def viewLeague(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    division1 = []
    division2 = []
    division3 = []
    division4 = []
    division5 = []
    division6 = []
    for team in team_list:
        if team.division == 1:
            division1.append(team)
        elif team.division == 2:
            division2.append(team)
        elif team.division == 3:
            division3.append(team)
        elif team.division == 4:
            division4.append(team)
        elif team.division == 5:
            division5.append(team)
        elif team.division == 6:
            division6.append(team)
        else:
            raise Http500
            
    return render_to_response('league/viewLeague.html', {'league':league, 'user':request.user,'profile':request.user.get_profile(),'player_list':player_list, 'team_list':team_list,'division1':division1,'division2':division2,'division3':division3,'division4':division4,'division5':division5,'division6':division6}, context_instance=RequestContext(request))

@login_required
def viewSchedule(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    player_list = request.user.get_profile().players.all()
    team_list = request.user.get_profile().teams.all()
    games_div1 = []
    games_div2 = []
    games_div3 = []
    games_div4 = []
    games_div5 = []
    games_div6 = []
    games_div1_completed = []
    games_div2_completed = []
    games_div3_completed = []
    games_div4_completed = []
    games_div5_completed = []
    games_div6_completed = []

    for teamseason in league.standings.all():
        for game in teamseason.reg_games.order_by('datetime'):
            if game.home_team.division == 1:
                if game.is_completed:
                    games_div1_completed.append(game)
                else:
                    games_div1.append(game)
            elif game.home_team.division == 2:
                if game.is_completed:
                    games_div2_completed.append(game)
                else:
                    games_div2.append(game)
            elif game.home_team.division == 3:
                if game.is_completed:
                    games_div3_completed.append(game)
                else:
                    games_div3.append(game)
            elif game.home_team.division == 4:
                if game.is_completed:
                    games_div4_completed.append(game)
                else:
                    games_div4.append(game)
            elif game.home_team.division == 5:
                if game.is_completed:
                    games_div5_completed.append(game)
                else:
                    games_div5.append(game)
            elif game.home_team.division == 6:
                if game.is_completed:
                    games_div6_completed.append(game)
                else:
                    games_div6.append(game)
            else:
                raise Http500
        games_all = games_div1 + games_div2 + games_div3 + games_div4 + games_div5 + games_div6
        games_all_completed = games_div1_completed + games_div2_completed + games_div3_completed + games_div4_completed + games_div5_completed + games_div6_completed            
            
        return render_to_response('league/schedule.html',{'user':request.user,'profile':request.user.get_profile(),'player_list':player_list,'team_list':team_list,'games_all':games_all,'games_all_completed':games_all_completed,'games_div1':games_div1,'games_div1_completed':games_div1_completed,'games_div2':games_div2,'games_div2_completed':games_div2_completed,'games_div3':games_div3,'games_div3_completed':games_div3_completed,'games_div4':games_div4,'games_div4_completed':games_div4_completed,'games_div5':games_div5,'games_div5_completed':games_div5_completed,'games_div6':games_div6,'games_div6_completed':games_div6_completed},context_instance=RequestContext(request))

        


@login_required
def scheduleNewSeason(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ScheduleNewSeasonForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                start_datetime = cd['start_datetime']
                league_list = League.objects.all()
                season_length = int(cd['season_length'])
                season_number = get_object_or_404(Team,pk=1).seasons.all().count()###Increment for each new season
                season_number = season_number if season_number > 0 else 1
                #season will last for 70 days
                #4 games (2 home, 2 away) against divisional teams
                #2 games (1 home, 1 away) against teams within conference
                #divison1,2,3 = conference1, divison4,5,6 = conference2
                #1 game against teams outside of conference.
                #if 10 teams out of conference then 5 home, 5 away
                #if odd number of outside of conference games, add game
                #i.e. if 15 teams out of conference, then 16 (8h,8a)games

                for league in league_list:
                    if not(league.is_full):
                        break
                    div1 = list(league.division1.all())
                    div2 = list(league.division2.all())
                    div3 = list(league.division3.all())
                    div4 = list(league.division4.all())
                    div5 = list(league.division5.all())
                    div6 = list(league.division6.all())
                    for team in league.teams.all():
                        team_season=TeamSeason(team=team,league=league,season_number=season_number)
                        team_season.save()
                        league.standings.add(team_season)
                        league.save()
                        team.seasons.add(team_season)
                        team.save()

                    #schedule games outside of conference
                    schedule_games_outside_conference(div1,div2,div3,div4,div5,div6,season_number,season_length,start_datetime)
                    #schedule games within conference
                    for team in div1:
                        team_season1 = team.seasons.get(season_number=season_number)
                        div1.remove(team)
                        schedule_games_within_conference(team_season1,div1,div2,div3,season_number,season_length,start_datetime)
                    for team in div2:
                        team_season1 = team.seasons.get(season_number=season_number)
                        div2.remove(team)
                        schedule_games_within_conference(team_season1,div2,div3,div1,season_number,season_length,start_datetime)
                    for team in div3:
                        team_season1 = team.seasons.get(season_number=season_number)
                        div3.remove(team)
                        schedule_games_within_conference(team_season1,div3,div1,div2,season_number,season_length,start_datetime)
                    for team in div4:
                        team_season1 = team.seasons.get(season_number=season_number)
                        div4.remove(team)
                        schedule_games_within_conference(team_season1,div4,div5,div6,season_number,season_length,start_datetime)
                    for team in div5:
                        team_season1 = team.seasons.get(season_number=season_number)
                        div5.remove(team)
                        schedule_games_within_conference(team_season1,div5,div6,div4,season_number,season_length,start_datetime)
                    for team in div6:
                        team_season1 = team.seasons.get(season_number=season_number)
                        div6.remove(team)
                        schedule_games_within_conference(team_season1,div6,div4,div5,season_number,season_length,start_datetime)
                alert = "Season successfully scheduled with startdatetime of %s and season length of %s." % (start_datetime,season_length)
                return render_to_response('league/scheduleNewSeason.html',{'form':form,'user':request.user,'profile':request.user.get_profile(),'player_list':request.user.get_profile().players.all(),'team_list':request.user.get_profile().teams.all(),'alert':alert},context_instance=RequestContext(request))
        else:
            form = ScheduleNewSeasonForm()
        return render_to_response('league/scheduleNewSeason.html',{'form':form,'user':request.user,'profile':request.user.get_profile(),'player_list':request.user.get_profile().players.all(),'team_list':request.user.get_profile().teams.all()},context_instance=RequestContext(request))
                
    else:
        return render_to_response('404.html',{'user':request.user,'profile':request.user.get_profile(),'player_list':request.user.get_profile().players.all(),'team_list':request.user.get_profile().teams.all()},context_instance=RequestContext(request))


#@is_home : if team_season1's team is the home team for this game
def schedule_game(team_season1,team_season2,season_length,start_datetime,is_home):
    #calculate the day of a game
    daytime = start_datetime + timedelta(randrange(0,season_length))
    check_team1 = check_valid_day_team(team_season1,daytime)
    check_team2 = check_valid_day_team(team_season2,daytime)
    while (not(check_team1) or not(check_team2)):
        daytime = start_datetime + timedelta(randrange(0,season_length))
        check_team1 = check_valid_day_team(team_season1,daytime)
        check_team2 = check_valid_day_team(team_season2,daytime)
    game_datetime = datetime(daytime.year,daytime.month,daytime.day,randrange(11,22),10*randrange(0,6))
    if is_home:
        game = Game(home_team=team_season1.team,away_team=team_season2.team,is_playoff=False,datetime=game_datetime,has_started=False,is_completed=False)
        game.save()
        team_season1.reg_games.add(game)
        team_season1.save()
        team_season2.reg_games.add(game)
        team_season2.save()
    else:
        game = Game(home_team=team_season2.team,away_team=team_season1.team,is_playoff=False,datetime=game_datetime,has_started=False,is_completed=False)
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
    

def schedule_games_within_conference(team_season1,division,in_conf1,in_conf2,season_number,season_length,start_datetime):
    for team2 in division:
        team_season2 = team2.seasons.get(season_number=season_number)
        game1h = schedule_game(team_season1,team_season2,season_length,start_datetime,True)
        game2h = schedule_game(team_season1,team_season2,season_length,start_datetime,True)
        game3a = schedule_game(team_season1,team_season2,season_length,start_datetime,False)
        game4a = schedule_game(team_season1,team_season2,season_length,start_datetime,False)
    for team2 in in_conf1:
        team_season2 = team2.seasons.get(season_number=season_number)
        game1h = schedule_game(team_season1,team_season2,season_length,start_datetime,True)
        game2a = schedule_game(team_season1,team_season2,season_length,start_datetime,False)
    for team2 in in_conf2:
        team_season2 = team2.seasons.get(season_number=season_number)
        game1h = schedule_game(team_season1,team_season2,season_length,start_datetime,True)
        game2a = schedule_game(team_season1,team_season2,season_length,start_datetime,False)
        
def schedule_games_outside_conference(div1,div2,div3,div4,div5,div6,season_number,season_length,start_datetime):
    conf1 = list(chain(div1,div2,div3))
    conf2 = list(chain(div4,div5,div6))
    for team in conf1:
        team_season1 = team.seasons.get(season_number=season_number)
        is_home=True
        team2 = 0
        team_season2 = ""
        for team2 in conf2:
            team_season2 = team2.seasons.get(season_number=season_number)
            game1 = schedule_game(team_season1,team_season2,season_length,start_datetime,is_home)
            is_home=not(is_home)
        #schedule the 16th out of conference game for team
        game2 = schedule_game(team_season1,team_season2,season_length,start_datetime,not(is_home))


#Sets up the variables needed for pagination
def pagination_vars(number,per_page,max_number):
    number = int(number)
    have_previous = False
    have_next = False
    next_number = number + per_page
    previous_number = number - per_page
    if max_number > number:
        have_next = True
    if number >= max_number:
        have_next = False
        have_previous = True
        number = max_number
    elif number < 0:
        number = 0
        have_previous = False
    if number <=25:
        have_previous = False
    return number,have_previous,have_next,previous_number,next_number
