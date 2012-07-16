from wuska.hockey.models import Game,PlayerGame,Goal,Penalty,Team,Player,PlayerSeason,TeamSeason
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils.timezone import utc
from random import randrange,uniform
from datetime import datetime,timedelta
from itertools import chain
from math import trunc

#round current time to 15 min increments
dt = datetime.now()
start_time = dt - timedelta(minutes=dt.minute % 15,seconds = dt.second, microseconds = dt.microsecond)

games_now = Game.objects.filter(datetime = start_time)

for game in games_now:
    start_game(game)
    


def start_game(game):
    game.has_started = True
    game.save()
    log = ""
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
    home_pp1f = [Player.objects.get(pk=home.pp1lw),Player.objects.get(pk=home.pp1c),Player.objects.get(pk=home.pp1rw),Player.objects.get(pk=home.pp1ld),Player.objects.get(pk=home.pp1rd)]
    home_pp2 = [Player.objects.get(pk=home.pp2lw),Player.objects.get(pk=home.pp2c),Player.objects.get(pk=home.pp2rw),Player.objects.get(pk=home.pp2ld),Player.objects.get(pk=home.pp2rd)]
    home_pk1 = [Player.objects.get(pk=home.pk1c),Player.objects.get(pk=home.pk1w),Player.objects.get(pk=home.pk1ld),Player.objects.get(pk=home.pk1rd)]
    home_pk2 = [Player.objects.get(pk=home.pk2c),Player.objects.get(pk=home.pk2w),Player.objects.get(pk=home.pk2ld),Player.objects.get(pk=home.pk2rd)]
    home_g = Player.objects.get(pk=home.goalie1)

    home_lines = [home_line1,home_line2,home_line3,home_line4]
    home_pairings = [home_pair1,home_pair2,home_pair3]
    home_pp = [home_pp1,home_pp2]
    home_pk = [home_pk1,home_pk2]
    #Construct away lines
    away = game.away_team
    away_line1 = [Player.objects.get(pk=away.lw1),Player.objects.get(pk=away.c1),Player.objects.get(pk=away.rw1)]
    away_line2 = [Player.objects.get(pk=away.lw2),Player.objects.get(pk=away.c2),Player.objects.get(pk=away.rw2)]
    away_line3 = [Player.objects.get(pk=away.lw3),Player.objects.get(pk=away.c3),Player.objects.get(pk=away.rw3)]
    away_line4 = [Player.objects.get(pk=away.lw4),Player.objects.get(pk=away.c4),Player.objects.get(pk=away.rw4)]
    away_pair1 = [Player.objects.get(pk=away.defense1),Player.objects.get(pk=away.defense1)]
    away_pair2 = [Player.objects.get(pk=away.defense3),Player.objects.get(pk=away.defense4)]
    away_pair3 = [Player.objects.get(pk=away.defense5),Player.objects.get(pk=away.defense6)]
    away_pp1 = [Player.objects.get(pk=away.pp1lw),Player.objects.get(pk=away.pp1c),Player.objects.get(pk=away.pp1rw),Player.objects.get(pk=away.pp1ld),Player.objects.get(pk=away.pp1rd)]
    away_pp2 = [Player.objects.get(pk=away.pp2lw),Player.objects.get(pk=away.pp2c),Player.objects.get(pk=away.pp2rw),Player.objects.get(pk=away.pp2ld),Player.objects.get(pk=away.pp2rd)]
    away_pk1 = [Player.objects.get(pk=away.pk1c),Player.objects.get(pk=away.pk1w),Player.objects.get(pk=away.pk1ld),Player.objects.get(pk=away.pk1rd)]
    away_pk2 = [Player.objects.get(pk=away.pk2c),Player.objects.get(pk=away.pk2w),Player.objects.get(pk=away.pk2ld),Player.objects.get(pk=away.pk2rd)]
    away_g = Player.objects.get(pk=away.goalie1)

    away_lines = [away_line1,away_line2,away_line3,away_line4]
    away_pairings = [away_pair1,away_pair2,away_pair3]
    away_pp = [away_pp1,away_pp2]
    away_pk = [away_pk1,away_pk2]
    #create playerGames for all players, if player does not have a player season, then create one for them
    season_number = home.seasons.filter('-season_number')[0].season_number
    player_games_home = {}
    for player in home.players.all():
        pg = PlayerGame(player_id = player.id,game = game)
        pg.save()
        player_games_home[player.id]=pg
        if player.seasons.filter(season=season_number).count() == 0:
            ps = PlayerSeason(player.id,home.id,season=season_number)
            ps.save()
        ps = player.seasons.filter(season=season_number)[0]
        ps.games.add(pg)
        ps.save()
    player_games_home.sorted()

    player_games_away = {}
    for player in away.players.all():
        pg = PlayerGame(player_id = player.id,game = game)
        pg.save()
        player_games_away[player.id]=pg
        if player.seasons.filter(season=season_number).count() == 0:
            ps = PlayerSeason(player.id,away.id,season=season_number)
            ps.save()
        ps = player.seasons.filter(season=season_number)[0]
        ps.games.add(pg)
        ps.save()
    player_games_away.sorted()

    num_faceoffs_p1 = randrange(15,25)
    num_faceoffs_p2 = randrange(15,25)
    num_faceoffs_p3 = randrange(15,25)
    #calculate percent of time that a line plays
    #away team, convention: fo=faceoffs, h = home, l1=line1, p1= pairing1
    fo_a_l1 = trunc(away.tactics.line1_time/60)
    fo_a_l2 = trunc(away.tactics.line2_time/60)
    fo_a_l3 = trunc(away.tactics.line3_time/60)
    fo_a_l4 = 100 - fo_a_l1 - fo_a_l2 - fo_a_l3
    fo_a_p1 = trunc(away.tactics.pairing1_time/60)
    fo_a_p2 = trunc(away.tactics.pairing2_time/60)
    fo_a_p3 = 100 - fo_a_p1 - fo_a_p2
    
    home_line_matches = [home.tactics.match_line1 - 1,home.tactics.match_line2 - 1,home.tactics.match_line3 - 1,home.tactics.match_line4 - 1]

    away_team_line = away_lines[0]
    away_team_pairing = away_pairings[0]
    home_team_line = home_lines[home_lines_matches[0]]
    home_team_pairing = home_pairings[0]

    zone = 1
    #first period
    while num_faceoffs_p1 > 0:
        num_faceoffs_p1 -= 1
        home_possession,player_w_puck,log = do_faceoff(home_team_line,home_team_pairing,player_games_home,away_team_line,away_team_pairing,player_games_away,log)
        no_stoppage = True
        while no_stoppage:
            if home_possession:
                no_stoppage,same_team_w_puck,player_w_puck,primary_assist,second_assist,is_home_penalty,is_away_penalty,zone,log = do_possession_even_strength(player_w_puck,home_team_line,home_team_pairing,player_games_home,away_team_line,away_team_pairing,away_g,player_games_away,log,zone)
            else:
                no_stoppage,same_team_w_puck,player_w_puck,primary_assist,second_assist,is_home_penalty,is_away_penalty,zone,log = do_possession_even_strength(player_w_puck,away_team_line,away_team_pairing,player_games_away,home_team_line,home_team_pairing,home_g,player_games_home,log,zone)
        
            

   # @ zone: 0 = defensive zone, 1 = neutral zone, 2 = offensive zone
def do_possession_even_strength(player_w_puck,primary_assist,second_assist,off_pairing,player_games_off,def_line,def_pairing,def_g,player_games_def,log,zone):
    off_penalty = get_line_penalty(off_line)
    def_penalty = get_line_penalty(def_line)
    
    off_line_pair_no_puck = off_line + off_pairing
    off_line_pair_no_puck.remove(player_w_puck)
    def_line_pair = def_line + def_pairing
    
    if zone == 0:
        #options: 1: pass in zone (15 %), 2: pass to neutral zone(40%), 3: stickhandle & skate to skate to neutral zone(40%), 4: penalty(5%)
        
        option_odds = get_line_offense(off_line) - get_line_defense(def_line) + 60
        if option_odds > 90:
            option_odds = 90
        elif option_odds < 10:
            option_odds = 10
         
        option = randrange(1,101)
        if option <= 15:
            #pass in the same zone (15% chance of happening)
            pass_to = off_line_pair_no_puck[randrange(0,4)]
            log += "<BR> %s attempts to pass the puck to %s." %(player_w_puck.name,pass_to.name)
            if randrange(1,101) > option_odds:
                #option was unsuccessful
                pass_to = def_line_pair[randrange(0,4)]
                log +="<BR> %s intercepts the puck." % (pass_to.name)
                home_pg = player_games_off[player_w_puck]
                home_pg.exp_passing -= 0.001
                home_pg.save()
                home_pg = player_games_off[pass_to]
                temp = randrange(0,3)
                if temp == 0:
                    home_pg.exp_positioning += 0.001
                elif temp == 1:
                    home_pg.exp_skating += 0.001
                else:
                    home_pg.exp_awareness += 0.001                  
                home_pg.save()
                #no_stoppage,same_team_w_puck,player_w_puck,primary_assist,second_assist,is_home_penalty,is_away_penalty,zone,log
                #zone should now be 2 (offensive zone)
                return False,False,pass_to,None,None,False,False,2,log
            else:
                #option was successful
                home_pg = player_games_off[player_w_puck]
                home_pg.exp_passing += 0.001
                home_pg.save()
                home_pg = player_games_off[pass_to]
                temp = randrange(0,3)
                if temp == 0:
                    home_pg.exp_positioning += 0.001
                elif temp == 1:
                    home_pg.exp_skating += 0.001
                else:
                    home_pg.exp_awareness += 0.001                  
                home_pg.save()
                second_assist = primary_assist
                primary_assist = player_w_puck
                return False,True,pass_to,primary_assist,second_assist,False,False,0,log
            

    
    



def do_faceoff(home_line,home_pairing,player_games_home,away_line,away_pairing,player_games_away,log):
    #calculate who wins the faceoff
    home_center = home_line[1]
    #chance of home center getting kicked out of faceoff circle:10%
    if randrange(1,11) == 1:
        if home_line[0].faceoff > home_line[2].faceoff:
            home_center = home_line[0]
        else:
            home_center = home_line[2]
        log+= "%s was kicked out of the faceoff circle and replaced by %s." %(home_line[1].name,home_center.name)
    away_center = away_line[1]
    if randrange(1,11) == 1:
        if away_line[0].faceoff > away_line[2].faceoff:
            away_center = away_line[0]
        else:
            away_center = away_line[2]
        log+= "<BR> %s is kicked out of the faceoff circle and replaced by %s." %(away_line[1].name,away_center.name)
    temp = (.8 * home_center.faceoff + .2 * home_center.strength) - (.8 * away_center.faceoff + .2 * away_center.strength)
    home_odds = 50 + temp 
    if temp > 90:
        home_odds = 90
    elif temp <10:
        home_odds = 10
    if randrange(1,101) <= home_odds:
        #home team won the faceoff, update stats
        home_pg = player_games_home[home_center.id]
        home_pg.faceoffs_taken += 1
        home_pg.faceoffs_won += 1
        home_pg.exp_faceoff += .001
        home_pg.save()
        away_pg = player_games_away[away_center.id]
        away_pg.faceoffs_taken += 1
        away_pg.save()
        log+= "<BR> %s wins the faceoff." % (home_center.name)
        p_w_puck = randrange(0,5)
        player_w_puck = home_line[p_w_puck] if p_w_puck < 3 else home_pairing[p_w_puck - 3]
        return True,player_w_puck,log
    else:
        #away team won the faceoff, update stats
        home_pg = player_games_home[home_center.id]
        home_pg.faceoffs_taken += 1
        home_pg.save()
        away_pg = player_games_away[away_center.id]
        away_pg.faceoffs_taken += 1
        away_pg.faceoffs_won += 1
        away_pg.exp_faceoff += .001
        away_pg.save()
        log+= "<BR> %s wins the faceoff." % (away_center.name)
        p_w_puck = randrange(0,5)
        player_w_puck = away_line[p_w_puck] if p_w_puck < 3 else away_pairing[p_w_puck - 3]
        return False,player_w_puck,log


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

def get_line_offense(line_list):
    #shooting should be individual player, so don't include
    #weighted average of skills
    passing = .25 * get_line_passing(line_list)
    stick_handling = .18 * get_line_stick_handling(line_list)
    positioning = .05 * get_line_positioning(line_list)
    skating = .14 * get_line_skating(line_list)
    strength = .14 * get_line_skating(line_list)
    awareness = .20 * get_line_awareness(line_list)
    leadership = .04 * get_line_leadership(line_list)
    return passing + stick_handling + positioning + skating + strength + awareness +leadership

def get_line_defense(line_list):
    stick_handling = .05 * get_line_stick_handling(line_list)
    checking = .21 * get_line_checking(line_list)
    positioning = .22 * get_line_positioning(line_list)
    skating= .14* get_line_skating(line_list)
    strength = .14 * get_line_strength(line_list)
    awareness = .20 * get_line_awareness(line_list)
    leadership = .04 * get_line_leadership(line_list)
    return stick_handling + checking + positioning + skating + strength + awareness + leadership

def get_line_offense_zone0(line_list):

def get_line_penalty(line_list):
    stick_handling = .125 * get_line_stick_handling(line_list)
    checking = .125 * get_line_checking(line_list)
    positioning = .30 * get_line_positioning(line_list)
    skating= .15* get_line_skating(line_list)
    awareness = .30 * get_line_awareness(line_list)
    return stick_handling + checking + positioning + skating + awareness
    
        


