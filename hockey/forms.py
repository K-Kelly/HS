from django import forms
from bootstrap.forms import *

class TeamForm(forms.Form):
    name = forms.CharField(max_length=40)
    abbreviation = forms.CharField(max_length=3, min_length=2)
    arena_name = forms.CharField(max_length=40)


class OfferPlayerContractForm(forms.Form):
    salary = forms.IntegerField(max_value=20000000, min_value=100000)
    length = forms.IntegerField(max_value=10, min_value=1)
    no_trade = forms.BooleanField(required=False)
    message = forms.CharField(max_length=2000, widget=forms.Textarea)


class MessageForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.Textarea)
    body = forms.CharField(max_length=3000, widget=forms.Textarea)


def make_edit_lines_form(player_list):
    class EditLinesForm(forms.Form):
        l_list = player_list.filter(position = "L")
        c_list = player_list.filter(position="C")
        r_list = player_list.filter(position="R")
        d_list = player_list.filter(position="D")
        g_list = player_list.filter(position="G")
        list_id = []
        list_name = []
        for player in l_list:
            list_id.append(player.id)
            list_name.append(player.name)
        l_choices = zip(list_id,list_name)  
        list_id = []
        list_name = []
        for player in c_list:
            list_id.append(player.id)
            list_name.append(player.name)
        c_choices = zip(list_id,list_name) 
        list_id = []
        list_name = []
        for player in r_list:
            list_id.append(player.id)
            list_name.append(player.name)
        r_choices = zip(list_id,list_name) 
        list_id = []
        list_name = []
        for player in d_list:
            list_id.append(player.id)
            list_name.append(player.name)
        d_choices = zip(list_id,list_name) 
        list_id = []
        list_name = []
        for player in g_list:
            list_id.append(player.id)
            list_name.append(player.name)
        g_choices = zip(list_id,list_name) 
        l1_field = forms.ChoiceField(choices=l_choices)
        c1_field = forms.ChoiceField(choices=c_choices)
        r1_field = forms.ChoiceField(choices=r_choices)
        d1_field = forms.ChoiceField(choices=d_choices)
        g1_field = forms.ChoiceField(choices=g_choices)
        l2_field = forms.ChoiceField(choices=l_choices)
        c2_field = forms.ChoiceField(choices=c_choices)
        r2_field = forms.ChoiceField(choices=r_choices)
        d2_field = forms.ChoiceField(choices=d_choices)
        g2_field = forms.ChoiceField(choices=g_choices)
        l3_field = forms.ChoiceField(choices=l_choices)
        c3_field = forms.ChoiceField(choices=c_choices)
        r3_field = forms.ChoiceField(choices=r_choices)
        d3_field = forms.ChoiceField(choices=d_choices)
        l4_field = forms.ChoiceField(choices=l_choices)
        c4_field = forms.ChoiceField(choices=c_choices)
        r4_field = forms.ChoiceField(choices=r_choices)
        d4_field = forms.ChoiceField(choices=d_choices)
        d5_field = forms.ChoiceField(choices=d_choices)
        d6_field = forms.ChoiceField(choices=d_choices)
    return EditLinesForm



