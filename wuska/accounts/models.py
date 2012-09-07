from django.db import models
from django.contrib.auth.models import User
from wuska.hockey.models import Player,Team,Message
from django.db.models.signals import post_save
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    accepted_eula = models.BooleanField()
    players = models.ManyToManyField(Player, related_name='UserProfile_players')
    teams_owned = models.ManyToManyField(Team, related_name='UserProfile_teams_owned')
    teams_gmed = models.ManyToManyField(Team, related_name='UserProfile_teams_gmed')
    teams = models.ManyToManyField(Team, related_name='UserProfile_teams')
    pucks = models.IntegerField(default = 300)
    messages = models.ManyToManyField(Message, related_name='UserProfile_messages')
    new_message = models.BooleanField()
    def __unicode__(self):
        return "%s's profile" % self.user
    def get_absolute_url(self):
        return "/users/%i/" %self.id

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
