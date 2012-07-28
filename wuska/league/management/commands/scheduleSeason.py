from django.core.management.base import BaseCommand
from wuska.hockey.models import *
from django.shortcuts import get_object_or_404
from django.utils.timezone import utc
from random import randrange
from datetime import datetime,timedelta
from time import strptime,mktime
from itertools import chain

class Command(BaseCommand):
    help = 'Schedules games for the next season. arg1:date time in form "mm/dd/yyyy HH:MM". arg2: seasonlength (integer)'      
    def handle(self, temp_datetime,season_length, **options):
        scheduleNewSeason(temp_datetime,int(season_length))
        self.stdout.write('Successfully scheduled a new season.')

def scheduleNewSeason(temp_datetime,season_length):
    #temp_datetime = "08/01/2012 14:30"   
    start_datetime = datetime.fromtimestamp(mktime(strptime(temp_datetime, "%m/%d/%Y %H:%M"))).replace(tzinfo=utc)
    #season_length = 70
    season_number = get_object_or_404(Team,pk=1).seasons.all().count()###Increment for each new season
    season_number = season_number if season_number > 0 else 1
                #4 games (2 home, 2 away) against divisional teams
                #2 games (1 home, 1 away) against teams within conference
                #divison1,2,3 = conference1, divison4,5,6 = conference2
                #1 game against teams outside of conference.
                #if 10 teams out of conference then 5 home, 5 away
                #if odd number of outside of conference games, add game
                #i.e. if 15 teams out of conference, then 16 (8h,8a)games
    for league in League.objects.all():
        if not(league.is_full):
            break
        league_teams = list(league.teams.all())
        for team in league.teams.all():
                        #Create new teamSeason for each team
            team_season1=TeamSeason(team=team,league=league,season_number=season_number)
            team_season1.save()
            league.standings.add(team_season1)
            league.season_number = season_number
            league.save()
            team.seasons.add(team_season1)
            team.save()
            second_out_of_conf = []
        for team in league.teams.all():
            league_teams.remove(team)
            team_season1 = team.seasons.get(season_number=season_number)
            is_home = True # if next out of conference game home or away
            has_second_out_of_conf = False #for 16th out of conference game
            for team2 in league_teams:
                team_season2 = team2.seasons.get(season_number=season_number)
                if team.id != team2.id:                           
                    if team.division == team2.division:
                                    #schedule 4(2 home, 2 away) division games
                        game1h = schedule_game(team_season1,team_season2,season_length,start_datetime,True)
                        game2h = schedule_game(team_season1,team_season2,season_length,start_datetime,True)
                        game3a = schedule_game(team_season1,team_season2,season_length,start_datetime,False)
                        game4a = schedule_game(team_season1,team_season2,season_length,start_datetime,False)
                    elif (team.division <= 3 and team2.division <= 3) or (team.division >3 and team2.division >3):
                                    #schedule 2(1 h, 1 a) conference games
                        game1h = schedule_game(team_season1,team_season2,season_length,start_datetime,True)
                        game2a = schedule_game(team_season1,team_season2,season_length,start_datetime,False)
                    else:
                                    #schedule 1 out of conference game
                        game1 = schedule_game(team_season1,team_season2,season_length,start_datetime,is_home)
                        is_home = not(is_home)
                        if not(has_second_out_of_conf) and not(team2 in second_out_of_conf):
                            has_second_out_of_conf = True
                            game1 = schedule_game(team_season1,team_season2,season_length,start_datetime,is_home)
                            is_home = not(is_home)

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
    game_datetime = datetime(daytime.year,daytime.month,daytime.day,randrange(14,24),10*randrange(0,6)).replace(tzinfo=utc)
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
 
