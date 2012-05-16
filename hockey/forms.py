from django import forms
from bootstrap.forms import *

class TeamForm(forms.Form):
    name = forms.CharField(max_length=40)
    abbreviation = forms.CharField(max_length=3, min_length=2)
    arena_name = forms.CharField(max_length=40)


class OfferPlayerContractForm(BootstrapForm):
    #class Meta:
    #   layout = (
    #        Fieldset( "Salary Per Season","Length","No Trade Clause", "Message",),
    #    )
    salary = forms.IntegerField(max_value=20000000, min_value=100000)
    length = forms.IntegerField(max_value=10, min_value=1)
    no_trade = forms.BooleanField(required=False)
    message = forms.CharField(max_length=2000, widget=forms.Textarea)


class MessageForm():
    title = forms.CharField(max_length=100, widget=forms.Textarea)
    body = forms.CharField(max_length=3000, widget=forms.Textarea)
