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


class PlayGame:
    def __init__(self,game):
        self.game = game
        self.game.has_started = True
        self.game.save()
        self.log = ""
        # Construct home lines
        # need to handle exceptions
        self.home = game.home_team
        self.home_line1 = [Player.objects.get(pk=self.home.lw1),Player.objects.get(pk=self.home.c1),Player.objects.get(pk=self.home.rw1)]
        self.home_line2 = [Player.objects.get(pk=self.home.lw2),Player.objects.get(pk=self.home.c2),Player.objects.get(pk=self.home.rw2)]
        self.home_line3 = [Player.objects.get(pk=self.home.lw3),Player.objects.get(pk=self.home.c3),Player.objects.get(pk=self.home.rw3)]
        self.home_line4 = [Player.objects.get(pk=self.home.lw4),Player.objects.get(pk=self.home.c4),Player.objects.get(pk=self.home.rw4)]
        self.home_pair1 = [Player.objects.get(pk=self.home.defense1),Player.objects.get(pk=self.home.defense1)]
        self.home_pair2 = [Player.objects.get(pk=self.home.defense3),Player.objects.get(pk=self.home.defense4)]
        self.home_pair3 = [Player.objects.get(pk=self.home.defense5),Player.objects.get(pk=self.home.defense6)]
        self.home_pp1f = [Player.objects.get(pk=self.home.pp1lw),Player.objects.get(pk=self.home.pp1c),Player.objects.get(pk=self.home.pp1rw),Player.objects.get(pk=self.home.pp1ld),Player.objects.get(pk=self.home.pp1rd)]
        self.home_pp2 = [Player.objects.get(pk=self.home.pp2lw),Player.objects.get(pk=self.home.pp2c),Player.objects.get(pk=self.home.pp2rw),Player.objects.get(pk=self.home.pp2ld),Player.objects.get(pk=self.home.pp2rd)]
        self.home_pk1 = [Player.objects.get(pk=self.home.pk1c),Player.objects.get(pk=self.home.pk1w),Player.objects.get(pk=self.home.pk1ld),Player.objects.get(pk=self.home.pk1rd)]
        self.home_pk2 = [Player.objects.get(pk=self.home.pk2c),Player.objects.get(pk=self.home.pk2w),Player.objects.get(pk=self.home.pk2ld),Player.objects.get(pk=self.home.pk2rd)]
        self.home_g = Player.objects.get(pk=self.home.goalie1)
         
        self.home_lines = [self.home_line1,self.home_line2,self.home_line3,self.home_line4]
        self.home_pairings = [self.home_pair1,self.home_pair2,self.home_pair3]
        self.home_pp = [self.home_pp1,self.home_pp2]
        self.home_pk = [self.home_pk1,self.home_pk2]
    #Construct away lines
        self.away = self.game.away_team
        self.away_line1 = [Player.objects.get(pk=self.away.lw1),Player.objects.get(pk=self.away.c1),Player.objects.get(pk=self.away.rw1)]
        self.away_line2 = [Player.objects.get(pk=self.away.lw2),Player.objects.get(pk=self.away.c2),Player.objects.get(pk=self.away.rw2)]
        self.away_line3 = [Player.objects.get(pk=self.away.lw3),Player.objects.get(pk=self.away.c3),Player.objects.get(pk=self.away.rw3)]
        self.away_line4 = [Player.objects.get(pk=self.away.lw4),Player.objects.get(pk=self.away.c4),Player.objects.get(pk=self.away.rw4)]
        self.away_pair1 = [Player.objects.get(pk=self.away.defense1),Player.objects.get(pk=self.away.defense1)]
        self.away_pair2 = [Player.objects.get(pk=self.away.defense3),Player.objects.get(pk=self.away.defense4)]
        self.away_pair3 = [Player.objects.get(pk=self.away.defense5),Player.objects.get(pk=self.away.defense6)]
        self.away_pp1 = [Player.objects.get(pk=self.away.pp1lw),Player.objects.get(pk=self.away.pp1c),Player.objects.get(pk=self.away.pp1rw),Player.objects.get(pk=self.away.pp1ld),Player.objects.get(pk=self.away.pp1rd)]
        self.away_pp2 = [Player.objects.get(pk=self.away.pp2lw),Player.objects.get(pk=self.away.pp2c),Player.objects.get(pk=self.away.pp2rw),Player.objects.get(pk=self.away.pp2ld),Player.objects.get(pk=self.away.pp2rd)]
        self.away_pk1 = [Player.objects.get(pk=self.away.pk1c),Player.objects.get(pk=self.away.pk1w),Player.objects.get(pk=self.away.pk1ld),Player.objects.get(pk=self.away.pk1rd)]
        self.away_pk2 = [Player.objects.get(pk=self.away.pk2c),Player.objects.get(pk=self.away.pk2w),Player.objects.get(pk=self.away.pk2ld),Player.objects.get(pk=self.away.pk2rd)]
        self.away_g = Player.objects.get(pk=self.away.goalie1)
         
        self.away_lines = [self.away_line1,self.away_line2,self.away_line3,self.away_line4]
        self.away_pairings = [self.away_pair1,self.away_pair2,self.away_pair3]
        self.away_pp = [self.away_pp1,self.away_pp2]
        self.away_pk = [self.away_pk1,self.away_pk2]
    #create playerGames for all players, if player does not have a player season, then create one for them
        self.season_number = self.home.seasons.filter('-season_number')[0].season_number
        self.player_games_home = {}
        for player in self.home.players.all():
            pg = PlayerGame(player_id = player.id,game = self.game)
            pg.save()
            self.player_games_home[player.id]=pg
            if player.seasons.filter(season=self.season_number).count() == 0:
                ps = PlayerSeason(player.id,home.id,season=self.season_number)
                ps.save()
            ps = player.seasons.filter(season=self.season_number)[0]
            ps.games.add(pg)
            ps.save()
        self.player_games_home.sorted()

        self.player_games_away = {}
        for player in self.away.players.all():
            pg = PlayerGame(player_id = player.id,game = self.game)
            pg.save()
            self.player_games_away[player.id]=pg
            if player.seasons.filter(season=self.season_number).count() == 0:
                ps = PlayerSeason(player.id,self.away.id,season=self.season_number)
                ps.save()
            ps = player.seasons.filter(season=season_number)[0]
            ps.games.add(pg)
            ps.save()
        self.player_games_away.sorted()
        #Number of faceoffs in each period
        self.num_faceoffs_p = randrange(15,25)
        #self.num_faceoffs_p2 = randrange(15,25)
        #self.num_faceoffs_p3 = randrange(15,25)
    #calculate percent of time that a line plays
    #away team, convention: fo=faceoffs, h = home, l1=line1, p1= pairing1
        self.fo_a_l1 = trunc(self.away.tactics.line1_time/60.0)
        self.fo_a_l2 = trunc(self.away.tactics.line2_time/60.0)
        self.fo_a_l3 = trunc(self.away.tactics.line3_time/60.0)
        self.fo_a_l4 = 100 - self.fo_a_l1 - self.fo_a_l2 - self.fo_a_l3
        self.fo_a_p1 = trunc(self.away.tactics.pairing1_time/60.0)
        self.fo_a_p2 = trunc(self.away.tactics.pairing2_time/60.0)
        self.fo_a_p3 = 100 - self.fo_a_p1 - self.fo_a_p2
         
        self.home_line_matches = [self.home.tactics.match_line1 - 1,self.home.tactics.match_line2 - 1,self.home.tactics.match_line3 - 1,self.home.tactics.match_line4 - 1]
         self.home_pp1_match_tactic = self.home.tactics.match_pp1
         self.home_pk1_match_tactic = self.home.tactics.match_pk1
         
         #Starting lines of the game (line 1 of away team vs home team's match)
         self.cur_away_line = self.away_lines[0]
         self.cur_away_pairing = self.away_pairings[0]
         self.cur_home_line = self.home_lines[self.home_lines_matches[0]]
         self.cur_home_pairing = self.home_pairings[0]

         self.home_goals = 0
         self.away_goals = 0
         self.period = 1
         #have a stoppage time always be time_bt_fo (time between faceoffs)
#time = 20 min * 60 seconds. start at 1197 to allow 3 seconds for faceoff
         self.time = 1197
         self.time_bt_fo = (1.0/self.num_faceoffs_p) * self.time
         
         self.zone = 1
         self.penalty = []
         
         self.player_w_puck = None
         self.primary_assist = None
         self.second_assist = None
         self.same_team_w_puck = False
         self.no_stoppage = True
         self.home_possession = True

         self.log = ""


    def play_game():
        while self.num_faceoffs_p > 0:
            self.num_faceoffs_p -= 1
            if len(self.penalty) == 0:
                do_faceoff()
            else:
                #TO DO Implement. Might not need this else
                test = "test"
                while self.no_stoppage:   
                     if self.home_possession:
                         do_possession_even_strength(game,player_w_puck,home_team_line,home_team_pairing,player_games_home,away_team_line,away_team_pairing,away_g,player_games_away,log,zone,period,time,time_bt_fo)
                     else:
                         do_possession_even_strength(game,player_w_puck,away_team_line,away_team_pairing,player_games_away,home_team_line,home_team_pairing,home_g,player_games_home,log,zone,period,time,time_bt_fo)
    

    #calculate who wins the faceoff
    def do_faceoff():
        home_center = self.cur_home_line[1]
        #chance of home center getting kicked out of faceoff circle:10%
        if randrange(1,11) == 1:
            if self.home_line[0].faceoff > self.home_line[2].faceoff:
                home_center = self.home_line[0]
            else:
                home_center = self.home_line[2]
            self.log+= "%s was kicked out of the faceoff circle and replaced by %s." %(self.home_line[1].name,home_center.name)
        away_center = self.away_line[1]
        #chance of away center getting kicked out of fo circle: 10%
        if randrange(1,11) == 1:
            if self.away_line[0].faceoff > self.away_line[2].faceoff:
                away_center = self.away_line[0]
            else:
                away_center = self.away_line[2]
            self.log+= "<BR> %s is kicked out of the faceoff circle and replaced by %s." %(self.away_line[1].name,away_center.name)
        temp = (.8 * home_center.faceoff + .2 * home_center.strength) - (.8 * away_center.faceoff + .2 * away_center.strength)
        home_odds = adjust_odds(50 + temp,90,10) 
        if randrange(1,101) <= home_odds:
            #home team won the faceoff, update stats
            home_pg = self.player_games_home[home_center.id]
            home_pg.faceoffs_taken += 1
            home_pg.faceoffs_won += 1
            home_pg.exp_faceoff += .001
            home_pg.save()
            away_pg = self.player_games_away[away_center.id]
            away_pg.faceoffs_taken += 1
            away_pg.save()
            self.log+= "<BR> %s wins the faceoff." % (home_center.name)
            p_w_puck = randrange(0,5)
            self.player_w_puck = self.home_line[p_w_puck] if p_w_puck < 3 else self.home_pairing[p_w_puck - 3]
            self.home_possession = True
        else:
            #away team won the faceoff, update stats
            home_pg = self.player_games_home[home_center.id]
            home_pg.faceoffs_taken += 1
            home_pg.save()
            away_pg = self.player_games_away[away_center.id]
            away_pg.faceoffs_taken += 1
            away_pg.faceoffs_won += 1
            away_pg.exp_faceoff += .001
            away_pg.save()
            self.log+= "<BR> %s wins the faceoff." % (away_center.name)
            p_w_puck = randrange(0,5)
            self.player_w_puck = self.away_line[p_w_puck] if p_w_puck < 3 else self.away_pairing[p_w_puck - 3]
            self.home_possession = False


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
