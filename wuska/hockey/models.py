from django.db import models
import datetime
# Create your models here.
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
    shooting = models.IntegerField()
    passing = models.IntegerField()
    stick_handling = models.IntegerField()
    checking = models.IntegerField()
    positioning = models.IntegerField()
    endurance = models.IntegerField()
    skating = models.IntegerField()
    strength = models.IntegerField()
    faceoff = models.IntegerField()
    fighting = models.IntegerField()
    awareness = models.IntegerField()
    leadership = models.IntegerField()
    helmet = models.IntegerField()
    gloves = models.IntegerField()
    shoulder_pads = models.IntegerField()
    pants = models.IntegerField()
    skates = models.IntegerField()
    stick = models.IntegerField()
    contracts = models.ManyToManyField('hockey.Contract', related_name = 'player_contracts')
    free_agent = models.BooleanField()
    messages = models.ManyToManyField('hockey.Message', related_name = 'player_messages')
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
        return "/arena/%i" % self.id

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
        return "/team/%i/statistics/%i" % (self.team_id, self.year)

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
    
    def __unicode__(self):
        return str(self.id)
    
    class Meta:
        ordering = ['team_id']

class Message(models.Model):
    sender_user_id = models.IntegerField()
    sender_player_id = models.IntegerField(blank=True, default="-1")
    sender_team_id = models.IntegerField(blank=True, default="-1")
    receiver_players = models.ManyToManyField(Player, related_name = 'receiver_players')
    receiver_team_id = models.IntegerField(blank=True, default="-1")
    title = models.CharField(max_length = 100)
    body = models.CharField(max_length = 2000)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['sender_user_id']

class Team(models.Model):
    name = models.CharField(max_length=35)
    owner = models.IntegerField()
    general_manager = models.IntegerField()
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
    messages = models.ManyToManyField('hockey.Message', related_name = 'team_messages')
    numLWNeed = models.IntegerField(blank=True,default="-1")
    numCNeed = models.IntegerField(blank=True,default="-1")
    numRWNeed = models.IntegerField(blank=True,default="-1")
    numDNeed = models.IntegerField(blank=True,default="-1")
    numGNeed = models.IntegerField(blank=True,default="-1")
    avgAge = models.DecimalField(max_digits=5,decimal_places=3,blank=True,default=-1)
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
    conference1 = models.ManyToManyField(Team, related_name = 'league_conference1')
    conference2 = models.ManyToManyField(Team, related_name = 'league_conference2')
    conference3 = models.ManyToManyField(Team, related_name = 'league_conference3')
    conference4 = models.ManyToManyField(Team, related_name = 'league_conference4')
    salary_cap = models.IntegerField()
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/league/%i/" % self.id

    class Meta:
        ordering = ['name']


