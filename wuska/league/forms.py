from django import forms
from wuska.hockey.models import Player,Team
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain

class ScheduleNewSeasonForm(forms.Form):
    start_datetime = forms.DateTimeField(label="Start Datetime (Ex: '10/25/2006 14:30')")
    season_length = forms.IntegerField(min_value=60,max_value=100,label="Season Length (must be greater than 60)",widget=forms.TextInput(attrs={'class':'span1'}))
