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
    home_pp1_match_tactic = home.tactics.match_pp1
    home_pk1_match_tactic = home.tactics.match_pk1

    away_team_line = away_lines[0]
    away_team_pairing = away_pairings[0]
    home_team_line = home_lines[home_lines_matches[0]]
    home_team_pairing = home_pairings[0]

    #have a stoppage time always be time_bt_fo (time between faceoffs)
    #time = 20 min * 60 seconds. start at 1197 to allow 3 seconds for faceoff
    time = 1197
    time_bt_fo = (1.0/num_faceoffs_p1) * time
    zone = 1
    penalty = None
    #first period
    while num_faceoffs_p1 > 0:
        num_faceoffs_p1 -= 1
        if penalty is None:
            home_possession,player_w_puck,log = do_faceoff(home_team_line,home_team_pairing,player_games_home,away_team_line,away_team_pairing,player_games_away,log)
        else:
            
        no_stoppage = True
        while no_stoppage:
            
            if home_possession:
                no_stoppage,same_team_w_puck,player_w_puck,primary_assist,second_assist,zone,log,time,penalty = do_possession_even_strength(game,player_w_puck,home_team_line,home_team_pairing,player_games_home,away_team_line,away_team_pairing,away_g,player_games_away,log,zone,period,time,time_bt_fo)
            else:
                no_stoppage,same_team_w_puck,player_w_puck,primary_assist,second_assist,zone,log,time,penalty = do_possession_even_strength(game,player_w_puck,away_team_line,away_team_pairing,player_games_away,home_team_line,home_team_pairing,home_g,player_games_home,log,zone,period,time,time_bt_fo)
        
          

  
   # @ zone: 0 = defensive zone, 1 = neutral zone, 2 = offensive zone
def do_possession_even_strength(game,player_w_puck,primary_assist,second_assist,off_line,off_pairing,player_games_off,def_line,def_pairing,def_g,player_games_def,log,zone,period,time,time_bt_fo):
    off_penalty = get_line_penalty(off_line)
    def_penalty = get_line_penalty(def_line)
    penalty_odds = def_penalty - off_penalty + 30
    penalty_odds = adjust_odds(penalty_odds,90,10)
    off_penalty_choices = ["Boarding","Clipping","Charging","Elbowing","High-sticking","Holding","Roughing","Kneeing","Tripping","Slashing","Goaltender Interference","Interference","Unsportsmanlike Conduct","Delay of Game (Puck over the glass)"]
    def_penalty_choices = ["Boarding","Clipping","Charging","Elbowing","High-sticking","Holding","Roughing","Kneeing","Tripping","Slashing","Goaltender Interference","Interference","Unsportsmanlike Conduct","Holding the Stick","Hooking","Cross-checking"]

    #TO DO: Handle major penalties
    
    off_line_pair_no_puck = off_line + off_pairing
    off_line_pair_no_puck.remove(player_w_puck)
    def_line_pair = def_line + def_pairing
    
    if zone == 0:
        #options: 1: pass in zone (15 %), 2: pass to neutral zone(40%), 3: stickhandle & skate to skate to neutral zone(40%), 4: penalty(5%)       
        option_odds = get_line_offense(off_line) - get_line_defense(def_line) + 50
        option_odds = adjust_odds(option_odds,90,10)  
        
        #calculate the which option the player takes
        option = randrange(1,101)
        if option <= 55:
            #pass in the same zone (15% chance of happening)
            #pass to neutral zone (40% chance of happening)
            pass_to = off_line_pair_no_puck[randrange(0,4)]
            log += "<BR> %s attempts to pass the puck to %s." %(player_w_puck.name,pass_to.name)
            if randrange(1,101) > option_odds:
                #option was unsuccessful
                pass_to = def_line_pair[randrange(0,5)]
                log += "<BR> %s intercepts the puck." % (pass_to.name)
                off_pg = player_games_off[player_w_puck.id]
                off_pg.exp_passing -= 0.001
                off_pg.save()
                def_pg = player_games_def[pass_to.id]
                temp = randrange(0,3)
                if temp == 0:
                    def_pg.exp_positioning += 0.001
                elif temp == 1:
                    def_pg.exp_skating += 0.001
                else:
                    def_pg.exp_awareness += 0.001                  
                def_pg.save()
                #no_stoppage,same_team_w_puck,player_w_puck,primary_assist,second_assist,zone,log,time,penalty
                if option <= 35:
                    #if option was <= 15 then was a pass to the same zone; if option <= 35 then it was a pass to the neutral zone but intercepted in the intercepting player's offensive zone(zone 2). There is a 50% (1/2 of 40% = 20 % so the range of (15,35]
                    return False,False,pass_to,None,None,2,log,time,None
                else:
                    #pass was to the neutral zone, and intercepted in the neutral zone
                    return False,False,pass_to,None,None,1,log,time,None
            else:
                #option was successful
                off_pg = player_games_off[player_w_puck.id]
                off_pg.exp_passing += 0.001
                off_pg.save()
                off_pg = player_games_off[pass_to.id]
                temp = randrange(0,3)
                if temp == 0:
                    off_pg.exp_positioning += 0.001
                elif temp == 1:
                    off_pg.exp_skating += 0.001
                else:
                    off_pg.exp_awareness += 0.001                  
                off_pg.save()
                second_assist = primary_assist
                primary_assist = player_w_puck
                if option <= 15:
                    #pass to the same zone
                    #no_stoppage,same_team_w_puck,player_w_puck,primary_assist,second_assist,is_home_penalty,is_away_penalty,zone,log,time,penalty
                    return False,True,pass_to,primary_assist,second_assist,0,log,time,None
                else:
                    #pass to neutral zone(zone 1)
                    return False,True,pass_to,primary_assist,second_assist,1,log,time,None

        elif option <= 95:
            #player with puck skates & stickhandles to neutral zone
            log += "<BR> %s attempts to skate the puck into the neutral zone." %(player_w_puck.name)
            if randrange(1,101) > option_odds:
                #option was unsuccessful
                def_player_w_puck = def_line_pair[randrange(0,5)]
                off_pg = player_games_off[player_w_puck.id]
                def_pg = player_games_def[def_player_w_puck.id]
                temp = randrange(0,4)
                if temp == 0:
                    log +="<BR> %s poke checks the puck loose and recovers it." % (def_player_w_puck.name)
                    off_pg.exp_stick_handling -= 0.001
                    def_pg.exp_positioning += 0.001
                elif temp == 1:
                    log +="<BR> %s steals the puck." % (def_player_w_puck.name)
                    off_pg.exp_skating -= 0.001
                    def_pg.exp_skating += 0.001
                elif temp == 2:
                    log +="<BR> %s is checked into the boards and loses the puck to %s." % (player_w_puck.name,def_player_w_puck.name)
                    off_pg.exp_strength -= 0.001
                    def_pg.checks += 1
                    def_pg.exp_checking += 0.001
                else:
                    log +="<BR> %s loses the puck to %s." % (player_w_puck.name,def_player_w_puck.name)
                    off_pg.exp_awareness -= 0.001
                    def_pg.exp_awareness += 0.001                  
                off_pg.save()
                def_pg.save()
                #no_stoppage,same_team_w_puck,player_w_puck,primary_assist,second_assist,is_home_penalty,is_away_penalty,zone,log
                if randrange(0,2) == 0:
                    #puck interecepted in intercepting player's offensive zone
                    return False,False,def_player_w_puck,None,None,2,log,time,None
                else:
                    #puck intercepted in the neutral zone
                    return False,False,def_player_w_puck,None,None,1,log,time,None
            else:
                #option was successful
                off_pg = player_games_off[player_w_puck.id]
                temp = randrange(0,4)
                if temp == 0:
                    off_pg.stick_handling += 0.001
                elif temp == 1:
                    off_pg.exp_skating += 0.001
                elif temp == 2:
                    off_pg.exp_strength += 0.001
                else:
                    off_pg.exp_awareness += 0.001                  
                off_pg.save()
                #puck moves to neutral zone(zone 1)
                return False,True,player_w_puck,primary_assist,second_assist,1,log,time,None
        else:
            #penalty was committed
            time += time_bt_fo
            is_double_minor = True if randrange(1,101) < 5 else False
            if randrange(1,101) <= penalty_odds:
                #offensive team commits a penalty
                penalty_string = off_penalty_choices[randrange(0,len(off_penalty_choices))]
                offender = get_penalty_taker(off_line + off_pairing)
                penalty = Penalty(offender.id,offender.team_id,time,period,game,not(is_double_minor),is_double_minor,False,penalty_string)
            else:
                #defense team commits a penalty
                penalty_string = def_penalty_choices[randrange(0,len(def_penalty_choices))]
                offender = get_penalty_taker(def_line + def_pairing)
                penalty = Penalty(offender.id,offender.team_id,time,period,game,not(is_double_minor),is_double_minor,False,penalty_string)
            penalty.save()
            game.add(penalty)
            game.save()
            return True,False,None,None,None,2,log,time,penalty
            

def do_possession_penalty(game,player_w_puck,primary_assist,second_assist,off_line,off_pairing,player_games_off,def_line,def_pairing,def_g,player_games_def,log,zone,period,time,time_bt_fo):
    #create method for offensive skill on pk/pp and just use normal possession
    return None

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
    home_odds = adjust_odds(50 + temp,90,10) 
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

def get_penalty_taker(line_list):
    temp_sum = 0
    line_penalties = []
    for p in line_list:
        temp_sum += get_line_penalty([p])
        line_penalties.append(p)
    taker = randrange(1,temp_sum + 1)
    temp_sum = 0
    for i in range(len(a)):
        if taker <= temp_sum + line_penalties[i]:
            return line_list[i]
        temp_sum += line_penalties[i]  
    return line_list[i]

def get_line_penalty(line_list):
    stick_handling = .125 * get_line_stick_handling(line_list)
    checking = .125 * get_line_checking(line_list)
    positioning = .30 * get_line_positioning(line_list)
    skating= .15* get_line_skating(line_list)
    awareness = .30 * get_line_awareness(line_list)
    return stick_handling + checking + positioning + skating + awareness
    
def adjust_odds(odds,upper,lower):
    if odds > upper:
        odds = upper
    elif odds < lower:
        odds = lower
    return odds

def get_lines(away_team,last_line_away,away_lines_even,away_pairing_even,away_pp,away_pk,home_lines_even,home_pairings,home_pp,home_pk,home_line_matches,home_pp1_match,home_pk1_match,penalty_list):
    if penalty_list is None:
        #Use even strength lines
        a = 5
    else:
        #there is a penalty
        away_penalties = 0
        home_penalties = 0
        for penalty in penalty_list:
            if penalty.team_id == away_team.id:
                away_penalties += 1
            else:
                home_penalties += 1
        if away_penalties > home_penalties:
            #away team on penalty kill
            if last_line_away != away_pk[0]:
                return home_pp[home_pk1_match -1],away_pk[0]
            else:
                if (home_pk1_match - 1) == -1:
                    return home_pp[1],away_pk[1]
        elif away_penalties < home_penalties:
            #home team on penalty kill
            if last_line_away != away_pp[0]:
                return home_pk[home_pp1_match -1],away_pp[0]
            else:
                if (home_pp1_match - 1) == -1:
                    return home_pk[1],away_pp[1]
        else:
            #both teams on penalty kill

        
    #away_lines = [away_line1,away_line2,away_line3,away_line4]
    #away_pairings = [away_pair1,away_pair2,away_pair3]
    #away_pp = [away_pp1,away_pp2]
    #away_pk = [away_pk1,away_pk2]
    #home_lines = [home_line1,home_line2,home_line3,home_line4]
    home_pairings = [home_pair1,home_pair2,home_pair3]
    home_pp = [home_pp1,home_pp2]
    home_pk = [home_pk1,home_pk2]
    home_line_matches = [home.tactics.match_line1 - 1,home.tactics.match_line2 - 1,home.tactics.match_line3 - 1,home.tactics.match_line4 - 1]
