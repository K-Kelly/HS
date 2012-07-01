from django import forms
from wuska.hockey.models import Player,Team
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain

class ScheduleNewSeasonForm(forms.Form):
    start_datetime = forms.DateTimeField()
  
