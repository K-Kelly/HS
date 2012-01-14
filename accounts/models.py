from django.db import models
from django.contrib.auth.models import User
from hockey.models import *
from django.db.models.signals import post_save
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    accepted_eula = models.BooleanField()
    players = models.ManyToManyField(Player)
    teams = models.ManyToManyField(Team)
    pucks = models.IntegerField(default = 300)
    
    def __unicode__(self):
        return "%s's profile" % self.user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
