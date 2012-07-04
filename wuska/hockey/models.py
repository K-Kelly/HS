from django.db import models
import datetime

class Player(models.Model):
    team_id = models.IntegerField()
    user_id = models.IntegerField()
    name = models.CharField(max_length = 35)
    upgrades = models.SmallIntegerField()
    level = models.SmallIntegerField()
    experience = models.IntegerField()
    age = models.SmallIntegerField()
    retired = models.BooleanField()
    height = models.SmallIntegerField()
    weight = models.SmallIntegerField()
    salary = models.IntegerField()
    contract_end = models.SmallIntegerField()
    no_trade = models.BooleanField()
    position = models.CharField(max_length=1)
    style = models.SmallIntegerField()
    shooting = models.DecimalField(max_digits=5,decimal_places=3)
    passing = models.DecimalField(max_digits=5,decimal_places=3)
    stick_handling = models.DecimalField(max_digits=5,decimal_places=3)
    checking = models.DecimalField(max_digits=5,decimal_places=3)
    positioning = models.DecimalField(max_digits=5,decimal_places=3)
    endurance = models.DecimalField(max_digits=5,decimal_places=3)
    skating = models.DecimalField(max_digits=5,decimal_places=3)
    strength = models.DecimalField(max_digits=5,decimal_places=3)
    faceoff = models.DecimalField(max_digits=5,decimal_places=3)
    fighting = models.DecimalField(max_digits=5,decimal_places=3)
    awareness = models.DecimalField(max_digits=5,decimal_places=3)
    leadership = models.DecimalField(max_digits=5,decimal_places=3)
    helmet = models.SmallIntegerField()
    gloves = models.SmallIntegerField()
    shoulder_pads = models.SmallIntegerField()
    pants = models.SmallIntegerField()
    skates = models.SmallIntegerField()
    stick = models.SmallIntegerField()
    contracts = models.ManyToManyField('hockey.Contract', blank=True,related_name = 'player_contracts')
    free_agent = models.BooleanField()
    new_contract = models.BooleanField()
    datetime = models.DateTimeField(auto_now_add=True)
    seasons = models.ManyToManyField('hockey.PlayerSeason',blank=True,related_name = 'player_seasons')
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/player/%i/" %self.id

    class Meta:
        ordering = ['name']

class Arena(models.Model):
    name = models.CharField(max_length=50)
    occupancy = models.IntegerField()
    practice_facility = models.SmallIntegerField()
    locker_room = models.SmallIntegerField()
    equipment = models.SmallIntegerField()
    rink = models.SmallIntegerField()
    concessions = models.SmallIntegerField()
    lower_bowl = models.SmallIntegerField()
    mid_bowl = models.SmallIntegerField()
    upper_bowl = models.SmallIntegerField()
    box = models.SmallIntegerField()
    ticket_lower = models.SmallIntegerField()
    ticket_mid = models.SmallIntegerField()
    ticket_upper = models.SmallIntegerField()
    ticket_box = models.SmallIntegerField()
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/arena/%i/" % self.id

    class Meta:
        ordering = ['name']

class Contract(models.Model):
    player_id = models.IntegerField()
    team_id = models.IntegerField()
    team_name = models.CharField(max_length = 35)
    salary = models.IntegerField()
    length = models.SmallIntegerField()
    no_trade = models.BooleanField()
    message = models.CharField(max_length = 2000)
    is_accepted = models.BooleanField()
    datetime = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.id)
    
    class Meta:
        ordering = ['team_id']

class Message(models.Model):
    sender_user_id = models.IntegerField()
    sender_cc_users = models.ManyToManyField('accounts.UserProfile',blank=True,related_name='sender_cc_users')
    sender_player_id = models.IntegerField(blank=True, default="-1")
    sender_team_id = models.IntegerField(blank=True, default="-1")
    concerning_players = models.ManyToManyField(Player, blank=True,related_name = 'concerning_players')
    concerning_teams = models.ManyToManyField('hockey.Team', blank=True,related_name = 'concerning_teams')
    receiver_users = models.ManyToManyField('accounts.UserProfile',related_name = 'receiver_users')
    title = models.CharField(max_length = 100)
    body = models.CharField(max_length = 2000)
    is_automated = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['sender_user_id']

class Team(models.Model):
    name = models.CharField(max_length=35)
    owner = models.IntegerField()
    general_manager1 = models.IntegerField(blank=True, default="-1")
    general_manager2 = models.IntegerField(blank=True, default="-1")
    league_id = models.IntegerField()
    division = models.SmallIntegerField()
    arena = models.ForeignKey(Arena, related_name = 'team_arena')
    players = models.ManyToManyField(Player, blank=True,related_name = 'team_players')
    goalie1 = models.IntegerField(blank=True, default="-1")
    goalie2 = models.IntegerField(blank=True, default="-1")
    defense1 = models.IntegerField(blank=True, default="-1")
    defense2 = models.IntegerField(blank=True, default="-1")
    defense3 = models.IntegerField(blank=True, default="-1")
    defense4 = models.IntegerField(blank=True, default="-1")
    defense5 = models.IntegerField(blank=True, default="-1")
    defense6 = models.IntegerField(blank=True, default="-1")
    lw1 = models.IntegerField(blank=True, default="-1")
    lw2 = models.IntegerField(blank=True, default="-1")
    lw3 = models.IntegerField(blank=True, default="-1")
    lw4 = models.IntegerField(blank=True, default="-1")
    c1 = models.IntegerField(blank=True, default="-1")
    c2 = models.IntegerField(blank=True, default="-1")
    c3 = models.IntegerField(blank=True, default="-1")
    c4 = models.IntegerField(blank=True, default="-1")
    rw1 = models.IntegerField(blank=True, default="-1")
    rw2 = models.IntegerField(blank=True, default="-1")
    rw3 = models.IntegerField(blank=True, default="-1")
    rw4 = models.IntegerField(blank=True, default="-1")
    pp1lw = models.IntegerField(blank=True, default="-1")
    pp1c = models.IntegerField(blank=True, default="-1")
    pp1rw = models.IntegerField(blank=True, default="-1")
    pp1ld = models.IntegerField(blank=True, default="-1")
    pp1rd = models.IntegerField(blank=True, default="-1")
    pp2lw = models.IntegerField(blank=True, default="-1")
    pp2c = models.IntegerField(blank=True, default="-1")
    pp2rw = models.IntegerField(blank=True, default="-1")
    pp2ld = models.IntegerField(blank=True, default="-1")
    pp2rd = models.IntegerField(blank=True, default="-1")
    pk1c = models.IntegerField(blank=True, default="-1")
    pk1w = models.IntegerField(blank=True, default="-1")
    pk1ld = models.IntegerField(blank=True, default="-1")
    pk1rd = models.IntegerField(blank=True, default="-1")
    pk2c = models.IntegerField(blank=True, default="-1")
    pk2w = models.IntegerField(blank=True, default="-1")
    pk2ld = models.IntegerField(blank=True, default="-1")
    pk2rd = models.IntegerField(blank=True, default="-1")    
    funds = models.IntegerField()
    salary_used = models.IntegerField()
    salary_left = models.IntegerField()
    contracts = models.ManyToManyField(Contract, blank=True,related_name = 'team_contracts')
    numLWNeed = models.SmallIntegerField(blank=True,default="-1")
    numCNeed = models.SmallIntegerField(blank=True,default="-1")
    numRWNeed = models.SmallIntegerField(blank=True,default="-1")
    numDNeed = models.SmallIntegerField(blank=True,default="-1")
    numGNeed = models.SmallIntegerField(blank=True,default="-1")
    avgAge = models.DecimalField(max_digits=5,decimal_places=3,blank=True,default=-1)
    contract_status_change = models.BooleanField()
    seasons = models.ManyToManyField('hockey.TeamSeason',blank=True,related_name = 'team_teamseason')
    datetime = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/team/%i/" % self.id
    
    class Meta:
        ordering = ['name']


class League(models.Model):
    name = models.CharField(max_length=50)
    teams = models.ManyToManyField(Team, related_name = 'league_teams')
    season_number = models.SmallIntegerField(blank=True)
    #division1 = models.ManyToManyField(Team,blank=True,related_name = 'league_division1')
    #division2 = models.ManyToManyField(Team,blank=True, related_name = 'league_division2')
    #division3 = models.ManyToManyField(Team,blank=True,related_name = 'league_division3')
    #division4 = models.ManyToManyField(Team,blank=True, related_name = 'league_division4')
    #division5 = models.ManyToManyField(Team,blank=True, related_name = 'league_division5')
    #division6 = models.ManyToManyField(Team,blank=True, related_name = 'league_division6')
    salary_cap = models.IntegerField()
    standings = models.ManyToManyField('hockey.TeamSeason',blank=True, related_name = 'league_standings')
    datetime = models.DateTimeField(auto_now_add=True)
    is_full = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/league/%i/" % self.id

    class Meta:
        ordering = ['name']

class PlayerSeason(models.Model):
    player_id = models.IntegerField()
    team_id = models.IntegerField() #player's team at start of season
    games = models.ManyToManyField('hockey.PlayerGame',blank=True,related_name='playerseason_playergames')
    season = models.SmallIntegerField()


class TeamSeason(models.Model):
    #reg stands for Regular Season, po stands for Playoff
    team = models.ForeignKey(Team, related_name = 'teamseason_team')
    league = models.ForeignKey(League, related_name = 'teamseason_league')
    reg_games = models.ManyToManyField('hockey.Game',related_name = 'season_reg_games')
    po_games = models.ManyToManyField('hockey.Game',blank=True,related_name = 'season_po_games')
    reg_wins = models.SmallIntegerField(default=0)
    reg_losses = models.SmallIntegerField(default=0)
    over_wins = models.SmallIntegerField(default=0)
    over_losses = models.SmallIntegerField(default=0)
    so_wins = models.SmallIntegerField(default=0)
    so_losses = models.SmallIntegerField(default=0)
    po_wins = models.SmallIntegerField(default=0)
    po_losses = models.SmallIntegerField(default=0)
    is_over = models.BooleanField(default=False)
    statistics = models.ManyToManyField(PlayerSeason,blank=True,related_name='season_playerseason')
    datetime = models.DateField(auto_now_add=True)
    season_number = models.SmallIntegerField()
    
    def get_points(self):
        return (reg_wins + over_wins + so_wins) * 2 + over_losses + so_losses
    points = property(get_points)
    def __unicode__(self):
        return u'%s season: %s' % (self.team.name,self.season_number)

    def get_absolute_url(self):
        return "/season/%i/" % self.id

class Game(models.Model):
    home_team = models.ForeignKey(Team, related_name = 'game_home_team')
    away_team = models.ForeignKey(Team, related_name = 'game_away_team')
    is_playoff = models.BooleanField(default=False)
    datetime = models.DateTimeField()
    has_started = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    winning_team_id = models.IntegerField(default=-1)
    home_goals = models.ManyToManyField('hockey.Goal',blank=True,related_name = 'game_goals_home')
    away_goals = models.ManyToManyField('hockey.Goal',blank=True,related_name = 'game_goals_away')
    penalty = models.ManyToManyField('hockey.Penalty',blank=True,related_name = 'game_penalties')
    home_win = models.BooleanField(blank=True)
    overtime = models.BooleanField(blank=True)
    shootout = models.BooleanField(blank=True)
    summary = models.TextField(default="-1")
       
    def __unicode__(self):
        return u'%s at %s' % (self.away_team.name,self.home_team.name)

    def get_absolute_url(self):
        return "/game/%i/" % self.id

class PlayerGame(models.Model):
    player_id = models.IntegerField()
    game = models.ForeignKey('hockey.Game',related_name = 'playergame_game')
    points = models.ManyToManyField('hockey.Goal',blank=True,related_name = 'playergame_points')
    penalty = models.ManyToManyField('hockey.Penalty',blank=True,related_name = 'playergame_penalties')
    plus_minus = models.SmallIntegerField(default=0)
    shots = models.SmallIntegerField(default=0)
    faceoffs_taken = models.SmallIntegerField(default=0)
    faceoffs_won = models.SmallIntegerField(default=0)
    checks = models.SmallIntegerField(default=0)
    shots_blocked = models.SmallIntegerField(default=0)
         
    def __unicode__(self):
        return u'%s' % (self.player_id)

    def get_absolute_url(self):
        return "/playerGame/%i/" % self.id


class Goal(models.Model):
    scorer_id = models.IntegerField(default=-1)
    primary_assist_id = models.IntegerField(default=-1,blank=True)
    secondary_assist_id = models.IntegerField(default=-1,blank=True)
    powerplay = models.BooleanField()
    shorthanded = models.BooleanField()
    empty_net = models.BooleanField()
    game_winner = models.BooleanField()
    team_id = models.IntegerField(default=-1)
    time = models.SmallIntegerField(default=-1)
    period = models.SmallIntegerField(default=-1)
    game = models.OneToOneField(Game)

    def __unicode__(self):
        return u'%s(%s,%s) at %s of period %s' % (self.scorer_id,self.primary_assist_id,self.secondary_assist_id, self.time,self.period)

class Penalty(models.Model):
    player_id = models.IntegerField(default=-1)
    team_id = models.IntegerField(default=-1)
    time = models.SmallIntegerField(default=-1)
    period = models.SmallIntegerField(default=-1)
    game = models.OneToOneField(Game,related_name = "penalty_game")
    is_minor = models.BooleanField()
    is_double_minor = models.BooleanField()
    is_major = models.BooleanField()
    description = models.CharField(max_length=35)

    def __unicode__(self):
        return u'Penalty committed by %s' % (self.player_id)
