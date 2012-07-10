from wuska.hockey.models import Game,PlayerGame,Goal,Penalty,Team,Player,PlayerSeason,TeamSeason
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils.timezone import utc
from random import randrange
from datetime import datetime,timedelta
from itertools import chain

#round current time to 15 min increments
dt = datetime.now()
start_time = dt - timedelta(minutes=dt.minute % 15,seconds = dt.second, microseconds = dt.microsecond)

games_now = Game.objects.filter(datetime = start_time)

for game in games_now:
    start_game(game)
    




def start_game(game):
    game.has_started = True
    game.save()
    # Construct home lines
    # need to handle exceptions
    home = game.home_team
    home_line1 = [Player.objects.get(pk=home.lw1),Player.objects.get(pk=home.c1),Player.objects.get(pk=home.rw1)]
    home_line2 = [Player.objects.get(pk=home.lw2),Player.objects.get(pk=home.c2),Player.objects.get(pk=home.rw2)]
    home_line3 = [Player.objects.get(pk=home.lw3),Player.objects.get(pk=home.c3),Player.objects.get(pk=home.rw3)]
    home_line4 = [Player.objects.get(pk=home.lw4),Player.objects.get(pk=home.c4),Player.objects.get(pk=home.rw4)]
    home_pair1 = [Player.objects.get(pk=home.defense1),Player.objects.get(pk=home.defense1)]
    home_pair2 = [Player.objects.get(pk=home.defense3),Player.objects.get(pk=home.defense4)]
    home_pair3 = [Player.objects.get(pk=home.defense5),Player.objects.get(pk=home.defense6)]
    home_pp1f = [Player.objects.get(pk=home.pp1lw),Player.objects.get(pk=home.pp1c),Player.objects.get(pk=home.pp1rw)]
    home_pp1d = [Player.objects.get(pk=home.pp1ld),Player.objects.get(pk=home.pp1rd)]
    home_pp1f = [Player.objects.get(pk=home.pp1lw),Player.objects.get(pk=home.pp1c),Player.objects.get(pk=home.pp1rw)]
    home_pp1d = [Player.objects.get(pk=home.pp1ld),Player.objects.get(pk=home.pp1rd)]
    home_pp2f = [Player.objects.get(pk=home.pp2lw),Player.objects.get(pk=home.pp2c),Player.objects.get(pk=home.pp2rw)]
    home_pp2d = [Player.objects.get(pk=home.pp2ld),Player.objects.get(pk=home.pp2rd)]
    home_pk1 = [Player.objects.get(pk=home.pk1c),Player.objects.get(pk=home.pk1w),Player.objects.get(pk=home.pk1ld),Player.objects.get(pk=home.pk1rd)]
    home_pk2 = [Player.objects.get(pk=home.pk2c),Player.objects.get(pk=home.pk2w),Player.objects.get(pk=home.pk2ld),Player.objects.get(pk=home.pk2rd)]
    home_g = Player.objects.get(pk=home.goalie1)

    #Construct away lines
    away = game.away_team
    away_line1 = [Player.objects.get(pk=away.lw1),Player.objects.get(pk=away.c1),Player.objects.get(pk=away.rw1)]
    away_line2 = [Player.objects.get(pk=away.lw2),Player.objects.get(pk=away.c2),Player.objects.get(pk=away.rw2)]
    away_line3 = [Player.objects.get(pk=away.lw3),Player.objects.get(pk=away.c3),Player.objects.get(pk=away.rw3)]
    away_line4 = [Player.objects.get(pk=away.lw4),Player.objects.get(pk=away.c4),Player.objects.get(pk=away.rw4)]
    away_pair1 = [Player.objects.get(pk=away.defense1),Player.objects.get(pk=away.defense1)]
    away_pair2 = [Player.objects.get(pk=away.defense3),Player.objects.get(pk=away.defense4)]
    away_pair3 = [Player.objects.get(pk=away.defense5),Player.objects.get(pk=away.defense6)]
    away_pp1f = [Player.objects.get(pk=away.pp1lw),Player.objects.get(pk=away.pp1c),Player.objects.get(pk=away.pp1rw)]
    away_pp1d = [Player.objects.get(pk=away.pp1ld),Player.objects.get(pk=away.pp1rd)]
    away_pp1f = [Player.objects.get(pk=away.pp1lw),Player.objects.get(pk=away.pp1c),Player.objects.get(pk=away.pp1rw)]
    away_pp1d = [Player.objects.get(pk=away.pp1ld),Player.objects.get(pk=away.pp1rd)]
    away_pp2f = [Player.objects.get(pk=away.pp2lw),Player.objects.get(pk=away.pp2c),Player.objects.get(pk=away.pp2rw)]
    away_pp2d = [Player.objects.get(pk=away.pp2ld),Player.objects.get(pk=away.pp2rd)]
    away_pk1 = [Player.objects.get(pk=away.pk1c),Player.objects.get(pk=away.pk1w),Player.objects.get(pk=away.pk1ld),Player.objects.get(pk=away.pk1rd)]
    away_pk2 = [Player.objects.get(pk=away.pk2c),Player.objects.get(pk=away.pk2w),Player.objects.get(pk=away.pk2ld),Player.objects.get(pk=away.pk2rd)]
    away_g = Player.objects.get(pk=away.goalie1)

    season_number = home.seasons.filter('-season_number')[0].season_number
    player_games_home = []
    for player in home.players.all():
        pg = PlayerGame(player_id = player.id,game = game)
        pg.save()
        player_games_home.append(pg)
        if player.seasons.filter(season=season_number).count() == 0:
            ps = PlayerSeason(player.id,home.id,season=season_number)
            ps.save()
        ps = player.seasons.filter(season=season_number)[0]
        ps.games.add(pg)
        ps.save()

    player_games_away = []
    for player in away.players.all():
        pg = PlayerGame(player_id = player.id,game = game)
        pg.save()
        player_games_away.append(pg)
        if player.seasons.filter(season=season_number).count() == 0:
            ps = PlayerSeason(player.id,away.id,season=season_number)
            ps.save()
        ps = player.seasons.filter(season=season_number)[0]
        ps.games.add(pg)
        ps.save()


def get_line_passing(line_list):
    pas_sum = 0
    for p in line_list:
        pas_sum += p.passing
    return pas_sum / len(line_list)

def get_line_stick_handling(line_list):
    stk_sum = 0
    for p in line_list:
        stk_sum += p.stick_handling
    return stk_sum / len(line_list)

def get_line_checking(line_list):
    chk_sum = 0
    for p in line_list:
        chk_sum += p.checking
    return chk_sum / len(line_list)

def get_line_positioning(line_list):
    pos_sum = 0
    for p in line_list:
        pos_sum += p.positioning
    return pos_sum / len(line_list)

def get_line_skating(line_list):
    temp_sum = 0
    for p in line_list:
        temp_sum += p.skating
    return temp_sum / len(line_list)

def get_line_strength(line_list):
    temp_sum = 0
    for p in line_list:
        temp_sum += p.strength
    return temp_sum / len(line_list)

#faceoff should also use wingers
def get_line_faceoff(line_list):
    temp_sum = 0
    for p in line_list:
        temp_sum += p.faceoff
    return temp_sum / len(line_list)

def get_line_awareness(line_list):
    temp_sum = 0
    for p in line_list:
        temp_sum += p.awareness
    return temp_sum / len(line_list)

def get_line_leadership(line_list):
    temp_sum = 0
    for p in line_list:
        temp_sum += p.leadership
    return temp_sum / len(line_list)


