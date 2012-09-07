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
from decimal import Decimal

class PlayGame:
    def __init__(self,game,season_number):
        self.game = game
        self.game.has_started = True
        self.game.save()
        self.log = ""
        # Construct the home lines
        # need to handle exceptions
        self.home = game.home_team
        self.home_line1 = [Player.objects.get(pk=self.home.lw1),Player.objects.get(pk=self.home.c1),Player.objects.get(pk=self.home.rw1)]
        self.home_line2 = [Player.objects.get(pk=self.home.lw2),Player.objects.get(pk=self.home.c2),Player.objects.get(pk=self.home.rw2)]
        self.home_line3 = [Player.objects.get(pk=self.home.lw3),Player.objects.get(pk=self.home.c3),Player.objects.get(pk=self.home.rw3)]
        self.home_line4 = [Player.objects.get(pk=self.home.lw4),Player.objects.get(pk=self.home.c4),Player.objects.get(pk=self.home.rw4)]
        self.home_pair1 = [Player.objects.get(pk=self.home.defense1),Player.objects.get(pk=self.home.defense1)]
        self.home_pair2 = [Player.objects.get(pk=self.home.defense3),Player.objects.get(pk=self.home.defense4)]
        self.home_pair3 = [Player.objects.get(pk=self.home.defense5),Player.objects.get(pk=self.home.defense6)]
        self.home_pp1 = [Player.objects.get(pk=self.home.pp1lw),Player.objects.get(pk=self.home.pp1c),Player.objects.get(pk=self.home.pp1rw),Player.objects.get(pk=self.home.pp1ld),Player.objects.get(pk=self.home.pp1rd)]
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
        self.season_number = season_number
        self.player_games_home = {}
        for player in self.home.players.all():
            pg = PlayerGame(player_id = player.id,game = self.game)
            pg.save()
            self.player_games_home[player.id]=pg
            if player.seasons.filter(season=self.season_number).count() == 0:
                ps = PlayerSeason(player_id = player.id,team_id = self.home.id,season=self.season_number)
                ps.save()
                player.seasons.add(ps)
                player.save()
            ps = player.seasons.filter(season=self.season_number)[0]
            ps.games.add(pg)
            ps.save()
        #self.player_games_home.sorted()

        self.player_games_away = {}
        for player in self.away.players.all():
            pg = PlayerGame(player_id = player.id,game = self.game)
            pg.save()
            self.player_games_away[player.id]=pg
            if player.seasons.filter(season=self.season_number).count() == 0:
                ps = PlayerSeason(player_id = player.id,team_id = self.away.id,season=self.season_number)
                ps.save()
                player.seasons.add(ps)
                player.save()
            ps = player.seasons.filter(season=season_number)[0]
            ps.games.add(pg)
            ps.save()
        #self.player_games_away.sorted()
        #Number of faceoffs in each period
        self.num_faceoffs_p = randrange(15,25)
        #calculate percent of time that a line plays
        #naming convention: fo=faceoffs, a = away, l1=line1, p1= pairing1
        self.fo_a_l1 = trunc(self.away.tactics.line1_time/60.0)
        self.fo_a_l2 = trunc(self.away.tactics.line2_time/60.0)
        self.fo_a_l3 = trunc(self.away.tactics.line3_time/60.0)
        self.fo_a_l4 = 100 - self.fo_a_l1 - self.fo_a_l2 - self.fo_a_l3
        self.fo_a_p1 = trunc(self.away.tactics.pairing1_time/60.0)
        self.fo_a_p2 = trunc(self.away.tactics.pairing2_time/60.0)
        self.fo_a_p3 = 100 - self.fo_a_p1 - self.fo_a_p2
        
        self.fo_h_p1 = trunc(self.home.tactics.pairing1_time/60.0)
        self.fo_h_p2 = trunc(self.home.tactics.pairing2_time/60.0)
        self.fo_h_p3 = 100 - self.fo_h_p1 - self.fo_h_p2

        self.home_line_matches = [self.home.tactics.match_line1 - 1,self.home.tactics.match_line2 - 1,self.home.tactics.match_line3 - 1,self.home.tactics.match_line4 - 1]
        self.home_pp1_match_tactic = self.home.tactics.match_pp1
        self.home_pk1_match_tactic = self.home.tactics.match_pk1
        
         #Starting lines of the game (line 1 of away team vs home team's match)
        self.cur_away_line = self.away_lines[0]
        self.cur_away_pairing = self.away_pairings[0]
        self.cur_home_line = self.home_lines[self.home_line_matches[0]]
        self.cur_home_pairing = self.home_pairings[0]
        
        self.home_goals = 0
        self.away_goals = 0
        self.period = 1
         #have a stoppage time always be time_bt_fo (time between faceoffs)
#time = 20 min * 60 seconds. start at 1197 to allow 3 seconds for faceoff
        self.time = 1197
        self.time_bt_fo = (1.0/self.num_faceoffs_p) * self.time
        
        self.zone = 1
        self.absolute_zone = 1
        self.penalty_list = []
    
        self.player_w_puck = None
        self.primary_assist = -1
        self.second_assist = -1
        self.same_team_w_puck = False
        self.no_stoppage = True
        self.home_possession = True
        
        self.log = ""
            
    def play_game(self):
        while self.num_faceoffs_p > 0:
            self.num_faceoffs_p -= 1
            self.do_faceoff()
            while self.no_stoppage:   
                if self.home_possession:
                    self.player_games_home,self.player_games_away = self.do_possession(self.cur_home_line,self.cur_home_pairing,self.player_games_home,self.cur_away_line,self.cur_away_pairing,self.away_g,self.player_games_away)
                else:
                    self.player_games_away,self.player_games_home = self.do_possession(self.cur_away_line,self.cur_away_pairing,self.player_games_away,self.cur_home_line,self.cur_home_pairing,self.home_g,self.player_games_home)
            #get the next lines
            self.get_lines()
        self.game.is_completed = True
        self.game.summary = self.log
        self.game.save()

    # @ zone: 0 = defensive zone, 1 = neutral zone, 2 = offensive zone
    def do_possession(self,off_line,off_pair,player_games_off,def_line,def_pair,def_g,player_games_def):
        #reset value of no_stoppage to True
        self.no_stoppage = True
        off_penalty = self.get_line_penalty(off_line)
        def_penalty = self.get_line_penalty(def_line)
        penalty_odds = def_penalty - off_penalty + 30
        penalty_odds = self.adjust_odds(penalty_odds,90,10)
        off_penalty_choices = ["Boarding","Clipping","Charging","Elbowing","High-sticking","Holding","Roughing","Kneeing","Tripping","Slashing","Interference","Unsportsmanlike Conduct"]
        def_penalty_choices = ["Boarding","Clipping","Charging","Elbowing","High-sticking","Holding","Roughing","Kneeing","Tripping","Slashing","Interference","Unsportsmanlike Conduct","Holding the Stick","Hooking","Cross-checking"]
        if self.zone == 0:
            off_penalty_choices.append("Delay of Game (Puck over the glass)")
        elif self.zone == 2:
            off_penalty_choices.append("Goaltender Interference")
            def_penalty_choices.append("Goaltender Interference")
        
        #TO DO: Handle major penalties
        #TO DO: If penalty expires while in play, recalculate lines and start new possession, so have the zone methods return when it detects play exiting penalty box
        
        option_odds = self.get_line_offense(off_line) - self.get_line_defense(def_line) + 50
        option_odds = self.adjust_odds(option_odds,90,10) 
        if self.zone == 0:
            return self.do_zone0_possession(off_line,off_pair,player_games_off,def_line,def_pair,player_games_def,penalty_odds,off_penalty_choices,def_penalty_choices,option_odds)
        elif self.zone == 1:
            return self.do_zone1_possession(off_line,off_pair,player_games_off,def_line,def_pair,player_games_def,penalty_odds,off_penalty_choices,def_penalty_choices,option_odds)
        else:
            return self.do_zone2_possession(off_line,off_pair,player_games_off,def_line,def_pair,def_g,player_games_def,penalty_odds,off_penalty_choices,def_penalty_choices,option_odds)
            
            
    def do_zone0_possession(self,off_line,off_pair,player_games_off,def_line,def_pair,player_games_def,penalty_odds,off_penalty_choices,def_penalty_choices,option_odds):
        off_line_pair_no_puck = off_line + off_pair
        off_line_pair_no_puck.remove(self.player_w_puck)
        def_line_pair = def_line + def_pair
        #options: 1: pass in zone (15 %), 2: pass to neutral zone(40%), 3: stickhandle & skate to skate to neutral zone(40%), 4: penalty(5%)                          
        #calculate which option the player takes
        option = randrange(1,101)
        if option <= 55:
            #pass in the same zone (15% chance of happening)
            #pass to neutral zone (40% chance of happening)
            pass_to = off_line_pair_no_puck[randrange(0,len(off_line_pair_no_puck))]
            self.log += "<BR> %s attempts to pass the puck to %s." %(self.player_w_puck.name,pass_to.name)
            if randrange(1,101) > option_odds:
                #option was unsuccessful
                pass_to = def_line_pair[randrange(0,len(def_line_pair))]
                self.log += "<BR> %s intercepts the puck." % (pass_to.name)
                off_pg = player_games_off[self.player_w_puck.id]
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
                player_games_off[self.player_w_puck.id] = off_pg
                player_games_def[pass_to.id] = def_pg
                if option <= 35:
                    #if option was <= 15 then was a pass to the same zone; if option <= 35 then it was a pass to the neutral zone but intercepted in the intercepting player's offensive zone(zone 2). There is a 50% (1/2 of 40% = 20 % so the range of (15,35]
                    self.zone = 2                        
                else:
                    #pass was to the neutral zone, and intercepted in the neutral zone
                    self.zone = 1
                self.same_team_w_puck = False
                self.home_possession = not(self.home_possession)
                self.player_w_puck = pass_to
                self.primary_assist = -1
                self.second_assist = -1
                return player_games_off,player_games_def                     
            else:
                #option was successful
                off_pg = player_games_off[self.player_w_puck.id]
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
                player_games_off[pass_to.id] = off_pg
                self.second_assist = self.primary_assist
                self.primary_assist = self.player_w_puck.id
                self.same_team_w_puck = True
                self.player_w_puck = pass_to
                if option <= 15:
                    #pass to the same zone
                    self.zone = 0
                else:
                    #pass to neutral zone(zone 1)
                    self.zone = 1
                return player_games_off,player_games_def

        elif option <= 95:
            #player with puck skates & stickhandles to neutral zone
            self.log += "<BR> %s attempts to skate the puck into the neutral zone." %(self.player_w_puck.name)
            if randrange(1,101) > option_odds:
                #option was unsuccessful
                def_player_w_puck = def_line_pair[randrange(0,len(def_line_pair))]
                off_pg = player_games_off[self.player_w_puck.id]
                def_pg = player_games_def[def_player_w_puck.id]
                temp = randrange(0,4)
                if temp == 0:
                    self.log +="<BR> %s poke checks the puck loose and recovers it." % (def_player_w_puck.name)
                    off_pg.exp_stick_handling -= 0.001
                    def_pg.exp_positioning += 0.001
                elif temp == 1:
                    self.log +="<BR> %s steals the puck." % (def_player_w_puck.name)
                    off_pg.exp_skating -= 0.001
                    def_pg.exp_skating += 0.001
                elif temp == 2:
                    self.log +="<BR> %s is checked into the boards and loses the puck to %s." % (self.player_w_puck.name,def_player_w_puck.name)
                    off_pg.exp_strength -= 0.001
                    def_pg.checks += 1
                    def_pg.exp_checking += 0.001
                else:
                    self.log +="<BR> %s loses the puck to %s." % (self.player_w_puck.name,def_player_w_puck.name)
                    off_pg.exp_awareness -= 0.001
                    def_pg.exp_awareness += 0.001                  
                off_pg.save()
                def_pg.save()
                player_games_off[self.player_w_puck.id] = off_pg
                player_games_def[def_player_w_puck.id] = def_pg
                self.same_team_w_puck = False
                self.home_possession = not(self.home_possession)
                self.player_w_puck = def_player_w_puck
                self.primary_assist = -1
                self.second_assist = -1
                if randrange(0,2) == 0:
                    #puck interecepted in intercepting player's offensive zone
                    self.zone = 2
                else:
                    #puck intercepted in the neutral zone
                    self.zone = 1
                return player_games_off,player_games_def
            else:
                #option was successful
                off_pg = player_games_off[self.player_w_puck.id]
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
                player_games_off[self.player_w_puck.id] = off_pg
                #puck moves to neutral zone(zone 1)
                self.zone = 1
                self.same_team_w_puck = True
                return player_games_off,player_games_def
        else:
            #penalty was committed
            temp = self.time - self.time_bt_fo
            self.time = temp if temp >= 0 else 0
            is_double_minor = True if randrange(1,101) < 5 else False
            if randrange(1,101) <= penalty_odds:
                #offensive team commits a penalty
                penalty_string = off_penalty_choices[randrange(0,len(off_penalty_choices))]
                offender = get_penalty_taker(off_line + off_pairing)
                penalty = Penalty(offender.id,offender.team_id,self.time,self.period,self.game,not(is_double_minor),is_double_minor,False,penalty_string)
            else:
                #defense team commits a penalty
                penalty_string = def_penalty_choices[randrange(0,len(def_penalty_choices))]
                offender = get_penalty_taker(def_line + def_pairing)
                penalty = Penalty(offender.id,offender.team_id,self.time,self.period,self.game,not(is_double_minor),is_double_minor,False,penalty_string)
            penalty.save()
            self.penalty_list.append(penalty)
            self.game.add(penalty)
            self.game.save()
            #no_stoppage,same_team_w_puck,player_w_puck,primary_assist,second_assist,is_home_penalty,is_away_penalty,zone,log
            self.no_stoppage = False
            self.player_w_puck = None
            self.primary_assist = -1
            self.second_assist = -1
            temp = "double " if is_double_minor else ""
            self.log += "<BR> A %s minor penalty is called against %s for %s." % (temp,offender.name,penalty_string)
            return player_games_off,player_games_def
    

    def do_zone1_possession(self,off_line,off_pair,player_games_off,def_line,def_pair,player_games_def,penalty_odds,off_penalty_choices,def_penalty_choices,option_odds):
        off_line_pair_no_puck = off_line + off_pair
        off_line_pair_no_puck.remove(self.player_w_puck)
        def_line_pair = def_line + def_pair
        #options: 1: pass in zone (15 %), 2: dump to offensive zone(40%), 3: stickhandle & skate to skate to neutral zone(40%), 4: penalty(5%)      
        #TO DO: base dump vs skate in on team tactics
        #calculate which option the player takes
        option = randrange(1,101)
        if option <= 15:
            #pass in the same zone (15% chance of happening)
            pass_to = off_line_pair_no_puck[randrange(0,len(off_line_pair_no_puck))]
            self.log += "<BR> %s attempts to pass the puck to %s." %(self.player_w_puck.name,pass_to.name)
            if randrange(1,101) > option_odds:
                #option was unsuccessful
                pass_to = def_line_pair[randrange(0,len(def_line_pair))]
                self.log += "<BR> %s intercepts the puck." % (pass_to.name)
                off_pg = player_games_off[self.player_w_puck.id]
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
                player_games_off[self.player_w_puck.id] = off_pg
                player_games_def[pass_to.id] = def_pg
                self.zone = 1
                self.same_team_w_puck = False
                self.home_possession = not(self.home_possession)
                self.player_w_puck = pass_to
                self.primary_assist = -1
                self.second_assist = -1
                return player_games_off,player_games_def                     
            else:
                #option was successful
                off_pg = player_games_off[self.player_w_puck.id]
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
                player_games_off[self.player_w_puck.id] = off_pg
                self.second_assist = self.primary_assist
                self.primary_assist = self.player_w_puck.id
                self.same_team_w_puck = True
                self.player_w_puck = pass_to
                self.zone = 1
                return player_games_off,player_games_def
        elif option <= 55:
            #player with puck dumps the puck in
            #3 outcomes: 1:dump successful and team retains possession of puck, 2: dump unsuccessful and team loses possession of puck, 3: icing
            self.log += "<BR> %s dumps the puck in." %(self.player_w_puck.name)
            if randrange(1,101) > option_odds:
                #option was unsuccessful
                def_player_w_puck = def_line_pair[randrange(0,len(def_line_pair))]
                player_chasing = off_line[randrange(0,len(off_line))]
                off_pg = player_games_off[self.player_w_puck.id]
                def_pg = player_games_def[def_player_w_puck.id]
                temp = randrange(0,10)
                if temp < 4:
                    if self.team_special_teams_multiplier(off_line) < 1:
                        #team is on the penalty kill, so icing is allowed
                        self.log +="<BR> %s clears the puck down the ice.  %s recovers the puck behind their net." % (self.player_w_puck.name, def_player_w_puck.name)
                    else:
                        temp2 = randrange(0,2)
                        if temp2 == 1:
                            self.log +="<BR> Icing! %s dumps the puck in before reaching the red line." % (def_player_w_puck.name)
                        else:
                            self.log +="<BR> Icing! %s dumps the puck in before reaching the red line.  %s chases down the puck, but %s reaches the puck first for icing." % (self.player_w_puck.name,player_chasing.name,def_player_w_puck.name)
                            def_pg.exp_skating += 0.001
                        off_pg.exp_awareness -= 0.001
                        self.no_stoppage = False
                        temp = self.time - self.time_bt_fo
                        self.time = temp if temp >= 0 else 0 
                        self.zone = 2 #offensive zone of team recovering puck
                        self.home_possession = not(self.home_possession)

                else:
                    self.log +="<BR> %s dumps the puck in and %s recovers the puck." % (self.player_w_puck.name,def_player_w_puck.name)
                    off_pg.exp_awareness -= 0.001
                    def_pg.exp_skating += 0.001
                    self.zone = 2
                    
                off_pg.save()
                def_pg.save()
                player_games_off[self.player_w_puck.id] = off_pg
                player_games_def[def_player_w_puck.id] = def_pg
                self.same_team_w_puck = False
                self.home_possession = not(self.home_possession)
                self.player_w_puck = def_player_w_puck
                self.primary_assist = -1
                self.second_assist = -1
                return player_games_off,player_games_def
            else:
                #dump is successful
                def_player_w_puck = def_line_pair[randrange(0,len(def_line_pair))]
                player_chasing = off_line[randrange(0,len(off_line))]
                off_pg = player_games_off[self.player_w_puck.id]
                off2_pg = player_games_off[player_chasing.id]
                self.log +="<BR> %s dumps the puck in and %s takes possession of the puck." % (self.player_w_puck.name,player_chasing.name)
                off_pg.exp_awareness += 0.001
                off2_pg.exp_skating += 0.001
                off_pg.save()
                off2_pg.save()
                player_games_off[self.player_w_puck.id] = off_pg
                player_games_def[player_chasing.id] = off2_pg
                self.zone = 2
                self.same_team_w_puck = True
                self.second_assist = self.primary_assist
                self.primary_assist = self.player_w_puck.id
                self.player_w_puck = player_chasing
                return player_games_off,player_games_def
                
        elif option <= 95:
            #player with puck skates & stickhandles to offensive zone
            self.log += "<BR> %s attempts to skate the puck into the offensive zone." %(self.player_w_puck.name)
            if randrange(1,101) > option_odds:
                #option was unsuccessful
                def_player_w_puck = def_line_pair[randrange(0,len(def_line_pair))]
                off_pg = player_games_off[self.player_w_puck.id]
                def_pg = player_games_def[def_player_w_puck.id]
                is_offside = False
                temp = randrange(0,5)
                if temp == 0:
                    self.log +="<BR> %s poke checks the puck loose and recovers it." % (def_player_w_puck.name)
                    off_pg.exp_stick_handling -= 0.001
                    def_pg.exp_positioning += 0.001
                elif temp == 1:
                    self.log +="<BR> %s steals the puck." % (def_player_w_puck.name)
                    off_pg.exp_skating -= 0.001
                    def_pg.exp_skating += 0.001
                elif temp == 2:
                    self.log +="<BR> %s is checked into the boards and loses the puck to %s." % (self.player_w_puck.name,def_player_w_puck.name)
                    off_pg.exp_strength -= 0.001
                    def_pg.checks += 1
                    def_pg.exp_checking += 0.001
                elif temp == 3:
                    self.log +="<BR> %s loses the puck to %s." % (self.player_w_puck.name,def_player_w_puck.name)
                    off_pg.exp_awareness -= 0.001
                    def_pg.exp_awareness += 0.001   
                elif temp == 4:
                    player_offside = off_line_pair_no_puck[randrange(0,len(off_line_pair_no_puck))]
                    self.log +="<BR> Offsides! %s moves into the offensive zone before the puck." % (player_offside.name)
                    t = randrange(1,11)
                    if t <= 4:
                        off_pg.exp_awareness -= 0.001
                    elif t <=7:
                        off_pg = player_games_off[player_offside.id]
                        off_pg.exp_awareness -= 0.001
                    else:
                        off_pg = player_games_off[player_offside.id]
                        off_pg.exp_skating -= 0.001
                    self.no_stoppage = False
                    temp = self.time - self.time_bt_fo
                    self.time = temp if temp >= 0 else 0 
                    is_offside = True
                off_pg.save()
                def_pg.save()
                player_games_off[self.player_w_puck.id] = off_pg
                player_games_def[def_player_w_puck.id] = def_pg
                self.same_team_w_puck = False
                self.home_possession = not(self.home_possession)
                self.player_w_puck = def_player_w_puck
                self.primary_assist = -1
                self.second_assist = -1
                if is_offside:
                    return player_games_off,player_games_def
                if randrange(0,2) == 0:
                    #puck interecepted in intercepting player's defensive zone
                    self.zone = 0
                else:
                    #puck intercepted in the neutral zone
                    self.zone = 1
                return player_games_off,player_games_def
            else:
                #option was successful
                off_pg = player_games_off[self.player_w_puck.id]
                temp = randrange(0,4)
                if temp == 0:
                    off_pg.exp_stick_handling += 0.001
                elif temp == 1:
                    off_pg.exp_skating += 0.001
                elif temp == 2:
                    off_pg.exp_strength += 0.001
                else:
                    off_pg.exp_awareness += 0.001                  
                off_pg.save()
                player_games_off[self.player_w_puck.id] = off_pg
                #puck moves to offensive zone(zone 2)
                self.zone = 2
                self.same_team_w_puck = True
                return player_games_off,player_games_def
        else:
            #penalty was committed
            temp = self.time - self.time_bt_fo
            self.time = temp if temp >= 0 else 0 
            is_double_minor = True if randrange(1,101) < 5 else False
            if randrange(1,101) <= penalty_odds:
                #offensive team commits a penalty
                penalty_string = off_penalty_choices[randrange(0,len(off_penalty_choices))]
                offender = self.get_penalty_taker(off_line + off_pairing)
                penalty = Penalty(offender.id,offender.team_id,self.time,self.period,self.game,not(is_double_minor),is_double_minor,False,penalty_string)
            else:
                #defense team commits a penalty
                penalty_string = def_penalty_choices[randrange(0,len(def_penalty_choices))]
                offender = self.get_penalty_taker(def_line + def_pair)
                penalty = Penalty(offender.id,offender.team_id,self.time,self.period,self.game,not(is_double_minor),is_double_minor,False,penalty_string)
            penalty.save()
            self.penalty_list.append(penalty)
            self.game.add(penalty)
            self.game.save()
            self.no_stoppage = False
            self.player_w_puck = None
            self.primary_assist = -1
            self.second_assist = -1
            temp = "double " if is_double_minor else ""
            self.log += "<BR> A %s minor penalty is called against %s for %s." % (temp,offender.name,penalty_string)
            return player_games_off,player_games_def


    def do_zone2_possession(self,off_line,off_pair,player_games_off,def_line,def_pair,def_g,player_games_def,penalty_odds,off_penalty_choices,def_penalty_choices,option_odds):
        off_line_pair_no_puck = off_line + off_pair
        off_line_pair_no_puck.remove(self.player_w_puck)
        def_line_pair = def_line + def_pair
        #What about breakaway?
        #TO DO: add penalty support
        """
        TO DO: split offensive zone into zones:
        -----------------------------blue line
        - 1           2           3 -
        -                           - 
        -                           -
        -                           -
        - 8   +      9        +   4 -
        -                           -
        -                           -
        -                           -
        --7-----------------------5--Goal line
         -           6             -
          -------------------------
        """
        pass_or_stick = self.adjust_odds(self.player_w_puck.passing - self.player_w_puck.stick_handling + 50,90,10)
        #choices are 0:shoot, 1:pass, 2:stickhandle
        choice = -1
        if randrange(1,101) <= pass_or_stick:
            #then passes, check if shoots
            choice = 1
            take_shot = self.adjust_odds(self.player_w_puck.shooting - self.player_w_puck.passing + 50,90,10)
            if randrange(1,101) <= take_shot:
                #then shoots
                choice = 0
        else:
            #then stickhandles
            choice = 2 
            take_shot = self.adjust_odds(self.player_w_puck.shooting - self.player_w_puck.stick_handling + 50,90,10)
            if randrange(1,101) <= take_shot:
                #then shoots
                choice = 0
        if choice == 0:
            def_player = def_pair[randrange(0,len(def_pair))]#TO DO: Find better way of determining who blocks shot
            is_blocked = self.adjust_odds(self.player_w_puck.shooting - def_player.positioning + 50,90,10)
            if randrange(1,101) <= is_blocked:
                #shot is not blocked, check if goal
                is_goal = self.adjust_odds(self.player_w_puck.shooting - self.get_goalie_save_skill(def_g) + 5,20,5)
                if randrange(1,101) <= is_goal:
                    #goal has been scored
                    is_pp,is_pk = self.is_pp_or_sh(self.player_w_puck)
                    temp = self.time - self.time_bt_fo
                    self.time = temp if temp >= 0 else 0
                    goal = Goal(scorer_id = self.player_w_puck.id,primary_assist_id=self.primary_assist,secondary_assist_id = self.second_assist,powerplay=is_pp,shorthanded=is_pk,empty_net=False,game_winner=False,team_id = self.player_w_puck.team_id,time=self.time,period=self.period,game=self.game)
                    goal.save()
                    if self.player_w_puck.team_id == self.home.id:
                        self.home_goals += 1
                        self.game.home_goals.add(goal)
                    else:
                        self.away_goals += 1
                        self.game.away_goals.add(goal)
                    self.game.save()
                    for player in (off_line + off_pair):
                        pg = player_games_off[player.id]
                        if is_pp:
                            remove_penalty(def_g.team_id)
                        else:
                            pg.plus_minus += 1
                        if player.id == self.player_w_puck.id:
                            pg.points.add(goal)
                            pg.shots += 1
                            pg.exp_shooting += .001                
                            player_games_def[def_player_w_puck.id] = def_pg
                        elif player.id == self.primary_assist or player.id == self.second_assist:
                            pg.points.add(goal)
                            pg.exp_passing += .001
                        pg.save()
                        player_games_off[player.id] = pg
                    for player in (def_line + def_pair):
                        pg = player_games_def[player.id]
                        if player.id == def_g:
                            pg.shots += 1
                        elif not(is_pp):
                            pg.plus_minus -= 1
                        pg.save()
                        player_games_def[player.id] = pg
                    self.zone = 1
                    self.no_stoppage = False
                    temp = self.time - self.time_bt_fo
                    self.time = temp if temp >= 0 else 0 
                    self.same_team_w_puck = False
                    self.player_w_puck = None
                    self.primary_assist = -1
                    self.second_assist = -1
                    #if on minor pp, then remove opposing player from penaltybox
                    return player_games_off,player_games_def
                else:
                    #goalie makes save
                    off_pg = player_games_off[self.player_w_puck.id]
                    off_pg.shots += 1
                    off_pg.exp_shooting += 1
                    off_pg.save()
                    player_games_off[self.player_w_puck.id] = off_pg
                    def_pg = player_games_def[def_g.id]
                    def_pg.shots += 1
                    def_pg.shots_blocked += 1
                    def_pg.save()
                    player_games_def[def_g.id] = def_pg
                    #calculate if goalie covers puck for faceoff
                    if randrange(1,101) <= 25:
                        #goalie covers puck for faceoff
                        self.no_stoppage = False
                        temp = self.time - self.time_bt_fo
                        self.time = temp if temp >= 0 else 0 
                        self.player_w_puck = None
                        self.primary_assist = -1
                    else:
                        #have goalie pass to a player
                        self.same_team_w_puck = False
                        self.home_possession = not(self.home_possession)
                        #do goalie pass to player, set player with puck to that player
                        self.primary_assist = def_g
                        self.player_w_puck = def_pair[randrange(0,len(def_pair))]
                    self.zone = 0
                    self.second_assist = -1
                    return player_games_off,player_games_def
            else:
                #shot is blocked
                off_pg = player_games_off[self.player_w_puck.id]
                off_pg.shots += 1
                off_pg.exp_awareness -= .001
                off_pg.save()
                player_games_off[self.player_w_puck.id] = off_pg
                def_pg = player_games_def[def_player.id]
                def_pg.shots_blocked += 1
                def_pg.exp_positioning += .001
                def_pg.save()
                player_games_def[def_g.id] = def_pg
                #player who blocks shot recovers puck (TODO: allow teammates to recover the puck or even other team)
                self.no_stoppage = False
                self.player_w_puck = def_player
                self.primary_assist = -1
                self.second_assist = -1
                self.zone = 0
                self.same_team_w_puck = False
                self.home_possession = not(self.home_possession)
                return player_games_off,player_games_def
        elif choice == 1:
            #player passes the puck
            #pass in the same zone (15% chance of happening)
            pass_to = off_line_pair_no_puck[randrange(0,len(off_line_pair_no_puck))]
            self.log += "<BR> %s attempts to pass the puck to %s." %(self.player_w_puck.name,pass_to.name)
            if randrange(1,101) > option_odds:
                #option was unsuccessful
                pass_to = def_line_pair[randrange(0,len(def_line_pair))]
                self.log += "<BR> %s intercepts the puck." % (pass_to.name)
                off_pg = player_games_off[self.player_w_puck.id]
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
                player_games_off[self.player_w_puck.id] = off_pg
                player_games_def[pass_to.id] = def_pg
                self.zone = 0
                self.same_team_w_puck = False
                self.home_possession = not(self.home_possession)
                self.player_w_puck = pass_to
                self.primary_assist = -1
                self.second_assist = -1
                return player_games_off,player_games_def                     
            else:
                #option was successful
                off_pg = player_games_off[self.player_w_puck.id]
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
                player_games_off[self.player_w_puck.id] = off_pg
                self.second_assist = self.primary_assist
                self.primary_assist = self.player_w_puck.id
                self.same_team_w_puck = True
                self.player_w_puck = pass_to
                self.zone = 2
                return player_games_off,player_games_def
        else:
            #stickhandle
            #player with puck skates & stickhandles in the offensive zone
            self.log += "<BR> %s attempts to stickhandle past the defense." %(self.player_w_puck.name)
            if randrange(1,101) > option_odds:
                #option was unsuccessful
                def_player_w_puck = def_line_pair[randrange(0,len(def_line_pair))]
                off_pg = player_games_off[self.player_w_puck.id]
                def_pg = player_games_def[def_player_w_puck.id]
                temp = randrange(0,4)
                if temp == 0:
                    self.log +="<BR> %s poke checks the puck loose and recovers it." % (def_player_w_puck.name)
                    off_pg.exp_stick_handling -= 0.001
                    def_pg.exp_positioning += 0.001
                elif temp == 1:
                    self.log +="<BR> %s steals the puck." % (def_player_w_puck.name)
                    off_pg.exp_skating -= 0.001
                    def_pg.exp_skating += 0.001
                elif temp == 2:
                    self.log +="<BR> %s is checked into the boards and loses the puck to %s." % (self.player_w_puck.name,def_player_w_puck.name)
                    off_pg.exp_strength -= 0.001
                    def_pg.checks += 1
                    def_pg.exp_checking += 0.001
                elif temp == 3:
                    self.log +="<BR> %s loses the puck to %s." % (self.player_w_puck.name,def_player_w_puck.name)
                    off_pg.exp_awareness -= 0.001
                    def_pg.exp_awareness += 0.001   
                off_pg.save()
                def_pg.save()
                player_games_off[self.player_w_puck.id] = off_pg
                player_games_def[def_player_w_puck.id] = def_pg
                self.same_team_w_puck = False
                self.home_possession = not(self.home_possession)
                self.player_w_puck = def_player_w_puck
                self.primary_assist = -1
                self.second_assist = -1
                self.zone = 0
                return player_games_off,player_games_def
            else:
                #option was successful
                off_pg = player_games_off[self.player_w_puck.id]
                temp = randrange(0,4)
                if temp == 0:
                    off_pg.exp_stick_handling += 0.001
                elif temp == 1:
                    off_pg.exp_skating += 0.001
                elif temp == 2:
                    off_pg.exp_strength += 0.001
                else:
                    off_pg.exp_awareness += 0.001                  
                off_pg.save()
                player_games_off[self.player_w_puck.id] = off_pg
                self.zone = 2
                self.same_team_w_puck = True
                return player_games_off,player_games_def

    #calculate who wins the faceoff
    def do_faceoff(self):
        home_center = self.cur_home_line[1]
        #chance of home center getting kicked out of faceoff circle:10%
        if randrange(1,11) == 1:
            if self.cur_home_line[0].faceoff > self.cur_home_line[2].faceoff:
                home_center = self.cur_home_line[0]
            else:
                home_center = self.cur_home_line[2]
            self.log+= "%s was kicked out of the faceoff circle and replaced by %s." %(self.cur_home_line[1].name,home_center.name)
        away_center = self.cur_away_line[1]
        #chance of away center getting kicked out of fo circle: 10%
        if randrange(1,11) == 1:
            if self.cur_away_line[0].faceoff > self.cur_away_line[2].faceoff:
                away_center = self.cur_away_line[0]
            else:
                away_center = self.cur_away_line[2]
            self.log+= "<BR> %s is kicked out of the faceoff circle and replaced by %s." %(self.cur_away_line[1].name,away_center.name)
        temp = (g_d(.8) * home_center.faceoff + g_d(.2) * home_center.strength) - (g_d(.8) * away_center.faceoff + g_d(.2) * away_center.strength)
        home_odds = self.adjust_odds(50 + temp,90,10) 
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
            self.player_w_puck = self.cur_home_line[p_w_puck] if p_w_puck < 3 else self.cur_home_pairing[p_w_puck - 3]
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
            self.player_w_puck = self.cur_away_line[p_w_puck] if p_w_puck < 3 else self.cur_away_pairing[p_w_puck - 3]
            self.home_possession = False


    def get_line_passing(self,line_list):
        pas_sum = 0
        for p in line_list:
            pas_sum += p.passing
        return pas_sum / len(line_list)

    def get_line_stick_handling(self,line_list):
        stk_sum = 0
        for p in line_list:
            stk_sum += p.stick_handling
        return stk_sum / len(line_list)

    def get_line_checking(self,line_list):
        chk_sum = 0
        for p in line_list:
            chk_sum += p.checking
        return chk_sum / len(line_list)

    def get_line_positioning(self,line_list):
        pos_sum = 0
        for p in line_list:
            pos_sum += p.positioning
        return pos_sum / len(line_list)

    def get_line_skating(self,line_list):
        temp_sum = 0
        for p in line_list:
            temp_sum += p.skating
        return temp_sum / len(line_list)

    def get_line_strength(self,line_list):
        temp_sum = 0
        for p in line_list:
            temp_sum += p.strength
        return temp_sum / len(line_list)

    def get_line_awareness(self,line_list):
        temp_sum = 0
        for p in line_list:
            temp_sum += p.awareness
        return temp_sum / len(line_list)

    def get_line_leadership(self,line_list):
        temp_sum = 0
        for p in line_list:
            temp_sum += p.leadership
        return temp_sum / len(line_list)

    def get_line_offense(self,line_list):
        #shooting should be individual player, so don't include
        #weighted average of skills
        #stunt offense if team shorthanded     
        passing = g_d(.25) * self.get_line_passing(line_list)
        stick_handling = g_d(.18) * self.get_line_stick_handling(line_list)
        positioning = g_d(.05) * self.get_line_positioning(line_list)
        skating = g_d(.14) * self.get_line_skating(line_list)
        strength = g_d(.14) * self.get_line_skating(line_list)
        awareness = g_d(.20) * self.get_line_awareness(line_list)
        leadership = g_d(.04) * self.get_line_leadership(line_list)
        multiplier = self.team_special_teams_multiplier(line_list)
        return (passing + stick_handling + positioning + skating + strength + awareness +leadership)*multiplier

    def get_line_defense(self,line_list):
        #stunt defence if team shorthanded
        stick_handling = g_d(.05) * self.get_line_stick_handling(line_list)
        checking = g_d(.21) * self.get_line_checking(line_list)
        positioning = g_d(.22) * self.get_line_positioning(line_list)
        skating= g_d(.14) * self.get_line_skating(line_list)
        strength = g_d(.14) * self.get_line_strength(line_list)
        awareness = g_d(.20) * self.get_line_awareness(line_list)
        leadership = g_d(.04) * self.get_line_leadership(line_list)
        multiplier = self.team_special_teams_multiplier(line_list)
        return (stick_handling + checking + positioning + skating + strength + awareness + leadership)*multiplier

    #removes a penalty after a powerplay goal
    def remove_penalty(self,team_id):
        penalty_to_remove = self.penalty_list = [0]
        for penalty in self.penalty_list:
            if penalty.team.id == team_id:
                self.penalty_list.remove(penalty)
                break
                
    #Returns: is_pp, is_pk             
    def is_pp_or_sh(self,player):
        num_away_penalty = 0
        num_home_penalty = 0
        for penalty in self.penalty_list:
            if penalty.team.id == self.home.id:
                num_home_penalty += 1
            else:
                num_away_penalty += 1
        if player.team_id == self.home.id:
            if num_home_penalty > num_away_penalty:
                return False,True
            elif num_home_penalty == num_away_penalty:
                return False,False
            else:
                return True,False
        else:
            #away team
            if num_away_penalty > num_home_penalty:
                return False,True
            elif num_away_penalty == num_home_penalty:
                return False,False
            else:
                return True,False
        

    #determines if team is on a pk or pp and then returns the multiplier to use for stunting skills.
    # if returns 1, then skill won't be stunted
    # return 1 if team is on the powerplay. Stunting only applied to penalty kill teams otherwise, there might be double bonus (bonus for being on pp and bonus gained from other team stunted)
    def team_special_teams_multiplier(self,line_list):
        num_away_penalty = 0
        num_home_penalty = 0
        for penalty in self.penalty_list:
            if penalty.team.id == self.home.id:
                num_home_penalty += 1
            else:
                num_away_penalty += 1
        if line_list[0].team_id == self.home.id:
            #line is home team
            if (num_home_penalty - num_away_penalty) >= 2:
                #team is on 3v5 penalty kill
                #stunt offence by 40%
                return .6
            elif (num_home_penalty - num_away_penalty) == 1:
                # teams is on a 4v5 penalty kill
                #stunt offence by 20%
                return .8
            else:
                # team is not on a penalty kill (might be 4v4 or 3v3 though)
                return 1
        else:
            #line is away team
            if (num_away_penalty - num_home_penalty) >= 2:
                #team is on 3v5 penalty kill
                #stunt offence by 40%
                return .6
            elif (num_away_penalty - num_home_penalty) == 1:
                # teams is on a 4v5 penalty kill
                #stunt offence by 20%
                return .8
            else:
                # team is not on a penalty kill (might be 4v4 or 3v3 though)
                return 1
        

    def get_penalty_taker(self,line_list):
        temp_sum = 0
        line_penalties = []
        for p in line_list:
            temp_sum += self.get_line_penalty([p])
            line_penalties.append(p)
        taker = randrange(1,temp_sum + 1)
        temp_sum = 0
        for i in range(len(a)):
            if taker <= temp_sum + line_penalties[i]:
                return line_list[i]
            temp_sum += line_penalties[i]  
        return line_list[i]

    def get_line_penalty(self,line_list):
        stick_handling = g_d(.125) * self.get_line_stick_handling(line_list)
        checking = g_d(.125) * self.get_line_checking(line_list)
        positioning = g_d(.30) * self.get_line_positioning(line_list)
        skating= g_d(.15)* self.get_line_skating(line_list)
        awareness = g_d(.30) * self.get_line_awareness(line_list)
        return stick_handling + checking + positioning + skating + awareness
    
    def adjust_odds(self,odds,upper,lower):
        if odds > upper:
            odds = upper
        elif odds < lower:
            odds = lower
        return odds
    def get_goalie_save_skill(self,goalie):
        #shooting = blocker side
        #passing = passing
        #stick_handling = Rebound control
        #checking = poke checking
        #positioning = stick side
        #skating = glove
        #strength = strength
        #faceoff = 5 hole
        #fighting = fighting
        #awareness = awareness
        #leadership = leadership
        temp = g_d(.19)*goalie.shooting + g_d(.19)*goalie.faceoff + g_d(.19)*goalie.positioning + g_d(.19)*goalie.skating + g_d(.23)*goalie.awareness + g_d(.01)*goalie.leadership
        return temp

    def get_goalie_rebound(self,goalie):
        #shooting = blocker side
        #passing = passing
        #stick_handling = Rebound control
        #checking = poke checking
        #positioning = stick side
        #skating = glove
        #strength = strength
        #faceoff = 5 hole
        #fighting = fighting
        #awareness = awareness
        #leadership = leadership
        temp = g_d(.76)*goalie.stick_handling + g_d(.12)*goalie.awareness + g_d(.12)*goalie.strength
        return temp
                                      

    def get_lines(self):
        if len(self.penalty_list) == 0:
            #Use even strength lines. May need to alter in future to prevent same line from playing consecutive faceoffs
            not_found_line = True
            line_away = None
            pair_away = None
            pair_home = None
            temp = randrange(1,101)
            if temp <= self.fo_a_l1:
                line_away = 0
            elif temp <= (self.fo_a_l1 + self.fo_a_l2):
                line_away = 1
            elif temp <= (self.fo_a_l1 + self.fo_a_l2 + self.fo_a_l3):
                line_away = 2
            else:
                line_away = 3
 
            temp = randrange(1,101)
            if temp <= self.fo_a_p1:
                pair_away = 0
            elif temp <= (self.fo_a_p1 + self.fo_a_p2):
                pair_away = 1
            else:
                pair_away = 2
            temp = randrange(1,101)
            if temp <= self.fo_h_p1:
                pair_home = 0
            elif temp <= (self.fo_h_p1 + self.fo_h_p2):
                pair_home = 1
            else:
                pair_home = 2
            
                #don't check if pair is last pair out since pairings can stay on for a while
            self.cur_away_line = self.away_lines[line_away]
            self.cur_away_pairing = self.away_pairings[pair_away]
            self.cur_home_line = self.home_lines[self.home_line_matches[line_away]]
            self.cur_home_pairing = self.home_pairings[pair_home]
        else:
            #there is a penalty
            #list of players who have taken a penalty
            home_players = []
            away_players = []
            for penalty in self.penalty_list:
                if penalty.team_id == away_team.id:
                    away_players.append(penalty.player)
                else:
                    home_players.append(penalty.player)
            if len(away_players) > len(home_players):
                #away team on penalty kill
                if self.cur_away_line != self.away_pk[0]:
                    line_choose = self.away_pk[0]
                    #make sure a player who has taken a penalty is not playing
                    for pen_player in away_players:
                        if pen_player in line_choose:
                            line_choose = find_replacement_player(pen_player,False,line_choose)
                    line_home = self.home_pp1 if self.home_pk1_match_tactic == 1 else self.home_pp2
                    for pen_player in home_players:
                        if pen_player in line_home:
                            line_home = find_replacement_player(pen_player,True,line_home)
                    self.cur_away_line = line_choose
                    self.cur_home_line = line_home
                else:
                    line_choose = self.away_pk[1]
                    for pen_player in away_players:
                        if pen_player in line_choose:
                            line_choose = find_replacement_player(pen_player,False,line_choose)
                    line_home = self.home_pp2 if self.home_pk1_match_tactic == 1 else self.home_pp1
                    for pen_player in home_players:
                        if pen_player in line_home:
                            line_home = find_replacement_player(pen_player,True,line_home)
                    self.cur_away_line = line_choose
                    self.cur_home_line = line_home
            elif len(away_players) > len(home_players):
                #home team on penalty kill
                if self.cur_away_line != self.away_pp[0]:
                    line_away = self.away_pp[0]
                    #in the case of away player being in penalty box
                    for pen_player in away_players:
                        if pen_player in line_away:
                            line_away = find_replacement_player(pen_player,False,line_away)
                    line_choose = self.home_pk1 if self.home_pp1_match_tactic == 1 else self.home_pk2
                    for pen_player in home_players:
                        if pen_player in line_choose:
                            line_choose = find_replacement_player(pen_player,True,line_choose)
                    self.cur_away_line = line_away
                    self.cur_home_line = line_choose
                else:
                    line_away = self.away_pp[1]
                    #in the case of away player being in penalty box
                    for pen_player in away_players:
                        if pen_player in line_away:
                            line_away = find_replacement_player(pen_player,False,line_away)         
                    line_choose = self.home_pk2 if self.home_pp1_match_tactic == 1 else self.home_pk1
                    for pen_player in home_players:
                        if pen_player in line_choose:
                            line_choose = find_replacement_player(pen_player,True,line_choose)
                    self.cur_away_line = line_away
                    self.cur_home_line = line_choose
            else:
                #both teams on penalty kill
                if self.cur_away_line != self.away_pk[0]:
                    line_away = self.away_pk[0]
                    for pen_player in away_players:
                        if pen_player in line_away:
                            line_away = find_replacement_player(pen_player,False,line_away)
                    line_home = self.home_pk1 if self.home_pk1_match_tactic == 1 else self.home_pk2                  
                    for pen_player in home_players:
                        if pen_player in line_home:
                            line_choose = find_replacement_player(pen_player,True,line_home)
                    self.cur_away_line = line_away
                    self.cur_home_line = line_home
                else:
                    line_away = self.away_pk[1]
                    for pen_player in away_players:
                        if pen_player in line_away:
                            line_away = find_replacement_player(pen_player,False,line_away)
                    line_home = self.home_pk2 if self.home_pk1_match_tactic == 1 else self.home_pk1                  
                    for pen_player in home_players:
                        if pen_player in line_home:
                            line_choose = find_replacement_player(pen_player,True,line_home)
                    self.cur_away_line = line_away
                    self.cur_home_line = line_home

        #Finds a replacement for a player currently serving a penalty.
    def find_replacement_player(self,player,is_home,line):
        index = line.index(player)
        need_loop = False
        if is_home:
            if player.position == "L":
                if player not in self.home_line1 and self.home_line1[0] not in self.penalty_list:
                    line.insert(index,self.home_line1[0])
                elif player not in self.home_line2 and self.home_line2[0] not in self.penalty_list:
                    line.insert(index,self.home_line2[0])
                elif player not in self.home_line3 and self.home_line3[0] not in self.penalty_list:
                    line.insert(index,self.home_line3[0])
                elif player not in self.home_line4 and self.home_line4[0] not in self.penalty_list:
                    line.insert(index,self.home_line4[0])
                else:
                    need_loop = True
            elif player.position == "C":
                if player not in self.home_line1 and self.home_line1[1] not in self.penalty_list:
                    line.insert(index,self.home_line1[1])
                elif player not in self.home_line2 and self.home_line2[1] not in self.penalty_list:
                    line.insert(index,self.home_line2[1])
                elif player not in self.home_line3 and self.home_line3[1] not in self.penalty_list:
                    line.insert(index,self.home_line3[1])
                elif player not in self.home_line4 and self.home_line4[1] not in self.penalty_list:
                    line.insert(index,self.home_line4[1])
                else:
                    need_loop = True
            elif player.position == "R":
                if player not in self.home_line1 and self.home_line1[2] not in self.penalty_list:
                    line.insert(index,self.home_line1[2])
                elif player not in self.home_line2 and self.home_line2[2] not in self.penalty_list:
                    line.insert(index,self.home_line2[2])
                elif player not in self.home_line3 and self.home_line3[2] not in self.penalty_list:
                    line.insert(index,self.home_line3[2])
                elif player not in self.home_line4 and self.home_line4[2] not in self.penalty_list:
                    line.insert(index,self.home_line4[2])
                else:
                    need_loop = True
            elif player.position == "D" and index == 2:
                if player not in self.home_pair1 and self.home_pair1[0] not in self.penalty_list:
                    line.insert(index,self.home_pair1[0])
                elif player not in self.home_pair2 and self.home_pair2[0] not in self.penalty_list:
                    line.insert(index,self.home_pair2[0])
                elif player not in self.home_pair3 and self.home_pair3[0] not in self.penalty_list:
                    line.insert(index,self.home_pair3[0])
                else:
                    need_loop = True
            else:
                if player not in self.home_pair1 and self.home_pair1[1] not in self.penalty_list:
                    line.insert(index,self.home_pair1[1])
                elif player not in self.home_pair2 and self.home_pair2[1] not in self.penalty_list:
                    line.insert(index,self.home_pair2[1])
                elif player not in self.home_pair3 and self.home_pair3[1] not in self.penalty_list:
                    line.insert(index,self.home_pair3[1])
                else:
                    need_loop = True
            if need_loop:
                home_players = self.home_line1 + self.home_line2 + self.home_line3 + self.home_line4 + self.home_pair1 + self.home_pair2 + self.home_pair3
                for p in home_players:
                    if player !=  p and p not in self.penalty_list:
                        line.insert(index,p)
                        return line
            else:
                return line
                
        else:
            if player.position == "L":
                if player not in self.away_line1 and self.away_line1[0] not in self.penalty_list:
                    line.insert(index,self.away_line1[0])
                elif player not in self.away_line2 and self.away_line2[0] not in self.penalty_list:
                    line.insert(index,self.away_line2[0])
                elif player not in self.away_line3 and self.away_line3[0] not in self.penalty_list:
                    line.insert(index,self.away_line3[0])
                elif player not in self.away_line4 and self.away_line4[0] not in self.penalty_list:
                    line.insert(index,self.away_line4[0])
                else:
                    need_loop = True
            elif player.position == "C":
                if player not in self.away_line1 and self.away_line1[1] not in self.penalty_list:
                    line.insert(index,self.away_line1[1])
                elif player not in self.away_line2 and self.away_line2[1] not in self.penalty_list:
                    line.insert(index,self.away_line2[1])
                elif player not in self.away_line3 and self.away_line3[1] not in self.penalty_list:
                    line.insert(index,self.away_line3[1])
                elif player not in self.away_line4 and self.away_line4[1] not in self.penalty_list:
                    line.insert(index,self.away_line4[1])
                else:
                    need_loop = True
            elif player.position == "R":
                if player not in self.away_line1 and self.away_line1[2] not in self.penalty_list:
                    line.insert(index,self.away_line1[2])
                elif player not in self.away_line2 and self.away_line2[2] not in self.penalty_list:
                    line.insert(index,self.away_line2[2])
                elif player not in self.away_line3 and self.away_line3[2] not in self.penalty_list:
                    line.insert(index,self.away_line3[2])
                elif player not in self.away_line4 and self.away_line4[2] not in self.penalty_list:
                    line.insert(index,self.away_line4[2])
                else:
                    need_loop = True
            elif player.position == "D" and index == 2:
                if player not in self.away_pair1 and self.away_pair1[0] not in self.penalty_list:
                    line.insert(index,self.away_pair1[0])
                elif player not in self.away_pair2 and self.away_pair2[0] not in self.penalty_list:
                    line.insert(index,self.away_pair2[0])
                elif player not in self.away_pair3 and self.away_pair3[0] not in self.penalty_list:
                    line.insert(index,self.away_pair3[0])
                else:
                    need_loop = True
            else:
                if player not in self.away_pair1 and self.away_pair1[1] not in self.penalty_list:
                    line.insert(index,self.away_pair1[1])
                elif player not in self.away_pair2 and self.away_pair2[1] not in self.penalty_list:
                    line.insert(index,self.away_pair2[1])
                elif player not in self.away_pair3 and self.away_pair3[1] not in self.penalty_list:
                    line.insert(index,self.away_pair3[1])
                else:
                    need_loop = True
            if need_loop:
                away_players = self.away_line1 + self.away_line2 + self.away_line3 + self.away_line4 + self.away_pair1 + self.away_pair2 + self.away_pair3
                for p in away_players:
                    if player !=  p and p not in self.penalty_list:
                        line.insert(index,p)
                        return line
            else:
                return line

#converts float to decimal. Stands for get_decimal
def g_d(a):
    return Decimal('%s'%a)
