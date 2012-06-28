from django.db import models
import datetime

class Player(models.Model):
    team_id = models.IntegerField()
    user_id = models.IntegerField()
    name = models.CharField(max_length = 35)
    upgrades = models.IntegerField()
    level = models.IntegerField()
    experience = models.IntegerField()
    age = models.IntegerField()
    retired = models.BooleanField()
    height = models.IntegerField()
    weight = models.IntegerField()
    salary = models.IntegerField()
    contract_end = models.IntegerField()
    no_trade = models.BooleanField()
    position = models.CharField(max_length=1)
    style = models.IntegerField()
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
    helmet = models.IntegerField()
    gloves = models.IntegerField()
    shoulder_pads = models.IntegerField()
    pants = models.IntegerField()
    skates = models.IntegerField()
    stick = models.IntegerField()
    contracts = models.ManyToManyField('hockey.Contract', related_name = 'player_contracts')
    free_agent = models.BooleanField()
    new_contract = models.BooleanField()
    datetime = models.DateTimeField(auto_now_add=True)
    goals = models.ManyToManyField('hockey.Goal',related_name = 'player_goals')
    assists = models.ManyToManyField('hockey.Goal',related_name = 'player_assists')
    penalties = models.ManyToManyField('hockey.Penalty',related_name = 'player_penalties')
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/player/%i/" %self.id

    class Meta:
        ordering = ['name']

class Arena(models.Model):
    name = models.CharField(max_length=50)
    occupancy = models.IntegerField()
    practice_Facility = models.IntegerField()
    locker_Room = models.IntegerField()
    equipment = models.IntegerField()
    rink = models.IntegerField()
    concessions = models.IntegerField()
    lower_bowl = models.IntegerField()
    mid_bowl = models.IntegerField()
    upper_bowl = models.IntegerField()
    box = models.IntegerField()
    ticket_lower = models.IntegerField()
    ticket_mid = models.IntegerField()
    ticket_upper = models.IntegerField()
    ticket_box = models.IntegerField()
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/arena/%i/" % self.id

    class Meta:
        ordering = ['name']

class team_statistics(models.Model):
    year = models.IntegerField()
    team_id = models.ForeignKey('hockey.Team')
    wins = models.IntegerField()
    losses = models.IntegerField()
    points = models.IntegerField()
    
    def __unicode__(self):
        return self.year

    def get_absolute_url(self):
        return "/team/%i/statistics/%i/" % (self.team_id, self.year)

    class Meta:
        ordering = ['year']

class Contract(models.Model):
    player_id = models.IntegerField()
    team_id = models.IntegerField()
    team_name = models.CharField(max_length = 35)
    salary = models.IntegerField()
    length = models.IntegerField()
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
    sender_cc_users = models.ManyToManyField('accounts.UserProfile',related_name='sender_cc_users')
    sender_player_id = models.IntegerField(blank=True, default="-1")
    sender_team_id = models.IntegerField(blank=True, default="-1")
    concerning_players = models.ManyToManyField(Player, related_name = 'concerning_players')
    concerning_teams = models.ManyToManyField('hockey.Team', related_name = 'concerning_teams')
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
    arena = models.ForeignKey(Arena, related_name = 'team_arena')
    players = models.ManyToManyField(Player, related_name = 'team_players')
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
    statistics = models.IntegerField(blank=True,default="-1")
    funds = models.IntegerField()
    salary_used = models.IntegerField()
    salary_left = models.IntegerField()
    contracts = models.ManyToManyField(Contract, related_name = 'team_contracts')
    numLWNeed = models.IntegerField(blank=True,default="-1")
    numCNeed = models.IntegerField(blank=True,default="-1")
    numRWNeed = models.IntegerField(blank=True,default="-1")
    numDNeed = models.IntegerField(blank=True,default="-1")
    numGNeed = models.IntegerField(blank=True,default="-1")
    avgAge = models.DecimalField(max_digits=5,decimal_places=3,blank=True,default=-1)
    contract_status_change = models.BooleanField()
    datetime = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/team/%i/" % self.id

    def tempPlayer():
        p = Player.objects.create(team_id = -1, user_id = -1, upgrades = 0, level = 0, experience = 0, name = "Computer", age = 18, retired = False, height = 60, weight = 175, salary =0, contract_end = 0, no_trade = True, position = "C", style = 0, shooting = 1, passing = 1, stickHandling = 1, checking =1, positioning = 1, endurance = 1, skating = 1, strength = 1, faceoff = 1, fighting = 1, awareness = 1, leadership = 1, helmet = 1, gloves = 1, shoulder_pads = 1, pants = 1, skates = 1, stick = 1)
        return p
    
    class Meta:
        ordering = ['name']


class League(models.Model):
    name = models.CharField(max_length=50)
    teams = models.ManyToManyField(Team, related_name = 'league_teams')
    division1 = models.ManyToManyField(Team, related_name = 'league_division1')
    division2 = models.ManyToManyField(Team, related_name = 'league_division2')
    division3 = models.ManyToManyField(Team, related_name = 'league_division3')
    division4 = models.ManyToManyField(Team, related_name = 'league_division4')
    division5 = models.ManyToManyField(Team, related_name = 'league_division5')
    division6 = models.ManyToManyField(Team, related_name = 'league_division6')
    salary_cap = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/league/%i/" % self.id

    class Meta:
        ordering = ['name']


class Game(models.Model):
    home_team = models.OneToOneField(Team, related_name = 'game_home_team')
    away_team = models.OneToOneField(Team, related_name = 'game_away_team')
    datetime = models.DateTimeField()
    has_started = models.BooleanField()
    is_completed = models.BooleanField()
    winning_team_id = models.IntegerField(default=-1)
    goals = models.ManyToManyField('hockey.Goal',related_name = 'game_goals')
    penalty = models.ManyToManyField('hockey.Penalty',related_name = 'game_penalties')
    
    def __unicode__(self):
        return u'%s at %s' % (self.away_team.name,self.home_team.name)

    def get_absolute_url(self):
        return "/game/%i/" % self.id

class Goal(models.Model):
    scorer_id = models.IntegerField(default=-1)
    primary_assist_id = models.IntegerField(default=-1,blank=True)
    secondary_assist_id = models.IntegerField(default=-1,blank=True)
    team_id = models.IntegerField(default=-1)
    time = models.IntegerField(default=-1)
    period = models.IntegerField(default=-1)
    game = models.OneToOneField(Game)

    def __unicode__(self):
        return u'%s(%s,%s) at %s of period %s' % (self.scorer_id,self.primary_assist_id,self.secondary_assist_id, self.time,self.period)

class Penalty(models.Model):
    player_id = models.IntegerField(default=-1)
    team_id = models.IntegerField(default=-1)
    time = models.IntegerField(default=-1)
    period = models.IntegerField(default=-1)
    game = models.OneToOneField(Game,related_name = "penalty_game")
    is_minor = models.BooleanField()
    is_double_minor = models.BooleanField()
    is_major = models.BooleanField()
    description = models.CharField(max_length=35)

    def __unicode__(self):
        return u'Penalty committed by %s' % (self.player_id)
