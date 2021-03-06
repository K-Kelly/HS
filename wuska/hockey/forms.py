from django import forms
from wuska.hockey.models import Player,Team
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain

class TeamForm(forms.Form):
    name = forms.CharField(max_length=40)
    abbreviation = forms.CharField(max_length=3, min_length=2)
    arena_name = forms.CharField(max_length=40)
    
    def clean_name(self):
        data = self.cleaned_data['name']
        if data.strip() == "":
            raise forms.ValidationError("A name consisting of only space(s) is not a valid Team name. Please try again with a different name.")
        else:
            num_team = Team.objects.filter(name__iexact=data).count()
            if num_team == 0:
                return data
            else:
                raise forms.ValidationError("A team named '%s' already exists. Please try again with a different name."%(data))
        return data

def get_management_form(gm1_name,gm2_name,owner_id):
    class TeamManagementForm(forms.Form):
        gm1_username = forms.CharField(max_length=50,label="Username of the General Manager",initial=gm1_name,required=False)
        gm2_username = forms.CharField(max_length=50,label="Username of the Assistant General Manager",initial=gm2_name,required=False)

        def clean_gm1_username(self):
            data = self.cleaned_data['gm1_username']           
            if data == "":
                return -1
            else:
                try:
                    gm1 = User.objects.get(username=data)
                    if gm1.id == owner_id:
                        raise forms.ValidationError("Owner can't also be a general manager. Leave the field blank if you don't want a general manager")
                    return gm1.id
                except ObjectDoesNotExist:
                    raise forms.ValidationError("Unable to find user %s"%(data))
        def clean_gm2_username(self):
            data = self.cleaned_data['gm2_username']
            if data == "":
                return -1
            else:
                try:
                    gm2 = User.objects.get(username=data)
                    if gm2.id == owner_id:
                        raise forms.ValidationError("Owner can't also be an assistant general manager. Leave the field blank if you don't want an assistant general manager")
                    return gm2.id
                except ObjectDoesNotExist:
                    raise forms.ValidationError("Unable to find user %s"%(data))

        def clean(self):
            cleaned_data = super(TeamManagementForm,self).clean()
            gm1 = cleaned_data.get("gm1_username")
            gm2 = cleaned_data.get("gm2_username")
            if gm1 == gm2 and gm1 != -1:
                raise forms.ValidationError("Management Change Unsuccessful: The General Manager and Assistant General Manager can't be the same user!")
            return cleaned_data

    return TeamManagementForm

class OfferPlayerContractForm(forms.Form):
    salary = forms.IntegerField(max_value=20000000, min_value=50000, label="Salary Per Year (Integer between 50000 and 20000000)",widget=forms.TextInput(attrs={'class':'span2'}))
    length = forms.IntegerField(max_value=10, min_value=1, label="Length of the Contract (Integer between 1 and 10)",widget=forms.TextInput(attrs={'class':'span1'}))
    no_trade = forms.BooleanField(required=False,label="No Trade Clause")
    message = forms.CharField(max_length=2000, widget=forms.Textarea(attrs={'class':'input-xlarge'}))


class MessageForm(forms.Form):
    title = forms.CharField(max_length=100,label="Title:",widget=forms.Textarea(attrs={'class':'input-xlarge','rows':'4'}))
    body = forms.CharField(max_length=3000,label="Body:",widget=forms.Textarea(attrs={'class':'input-xlarge','rows':'20'}))

def message_player(team_list):
    class MessagePlayerForm(forms.Form):
        title = forms.CharField(max_length=100,label="Title:",widget=forms.Textarea(attrs={'class':'input-xlarge','rows':'4'}))
        body = forms.CharField(max_length=3000,label="Body:",widget=forms.Textarea(attrs={'class':'input-xlarge','rows':'17'}))
        list_id = []
        list_name = []
        list_id.append(-1)
        list_name.append("Don't send from a team")
        for team in team_list:
            list_id.append(team.id)
            list_name.append(team.name)      
        team_choices = zip(list_id,list_name)
        team_field = forms.ChoiceField(choices=team_choices,label='Choose your team:',initial=-1)
    
        def clean_team_field(self):
            data = self.cleaned_data['team_field']
            data = int(data)
            if data == -1:
                return data
            for team in team_list:
                if team.id == data:
                    return data
            raise forms.ValidationError("You don't have access to this team.")  
    return MessagePlayerForm 
        
        
def make_edit_lines_form(player_list):
    class EditLinesForm(forms.Form):
        l_list = player_list.filter(position="L")
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
        forward_list = list(chain(l_list,c_list,r_list))
        list_id = []
        list_name = []
        for player in forward_list:
            list_id.append(player.id)
            list_name.append(player.name)
        pp_forward_choices = zip(list_id,list_name) 
        forward_defense_list = list(chain(forward_list,d_list))
        list_id = []
        list_name = []
        for player in forward_defense_list:
            list_id.append(player.id)
            list_name.append(player.name)
        pp_defense_choices = zip(list_id,list_name) 

        l1_field = forms.ChoiceField(choices=l_choices,label='Line 1 Left Wing')
        c1_field = forms.ChoiceField(choices=c_choices,label='Line 1 Center')
        r1_field = forms.ChoiceField(choices=r_choices,label='Line 1 Right Wing')
        d1_field = forms.ChoiceField(choices=d_choices,label='Pairing 1 Left Defense')
        g1_field = forms.ChoiceField(choices=g_choices,label='Starting Goalie')
        l2_field = forms.ChoiceField(choices=l_choices,label='Line 2 Left Wing')
        c2_field = forms.ChoiceField(choices=c_choices,label='Line 2 Center')
        r2_field = forms.ChoiceField(choices=r_choices,label='Line 2 Right Wing')
        d2_field = forms.ChoiceField(choices=d_choices,label='Pairing 1 Right Defense')
        g2_field = forms.ChoiceField(choices=g_choices,label='Backup Goalie')
        l3_field = forms.ChoiceField(choices=l_choices,label='Line 3 Left Wing')
        c3_field = forms.ChoiceField(choices=c_choices,label='Line 3 Center')
        r3_field = forms.ChoiceField(choices=r_choices,label='Line 3 Right Wing')
        d3_field = forms.ChoiceField(choices=d_choices,label='Pairing 2 Left Defense')
        l4_field = forms.ChoiceField(choices=l_choices,label='Line 4 Left Wing')
        c4_field = forms.ChoiceField(choices=c_choices,label='Line 4 Center')
        r4_field = forms.ChoiceField(choices=r_choices,label='Line 4 Right Wing')
        d4_field = forms.ChoiceField(choices=d_choices,label='Pairing 2 Right Defense')
        d5_field = forms.ChoiceField(choices=d_choices,label='Pairing 3 Left Defense')
        d6_field = forms.ChoiceField(choices=d_choices,label='Pairing 3 Right Defense')
        pp1l_field = forms.ChoiceField(choices=pp_forward_choices,label='PP1 Left Wing')
        pp1c_field = forms.ChoiceField(choices=pp_forward_choices,label='PP1 Center')
        pp1r_field = forms.ChoiceField(choices=pp_forward_choices,label='PP1 Right Wing')
        pp1ld_field = forms.ChoiceField(choices=pp_defense_choices,label='PP1 Left Defense')
        pp1rd_field = forms.ChoiceField(choices=pp_defense_choices,label='PP1 Right Defense')
        pp2l_field = forms.ChoiceField(choices=pp_forward_choices,label='PP2 Left Wing')
        pp2c_field = forms.ChoiceField(choices=pp_forward_choices,label='PP2 Center')
        pp2r_field = forms.ChoiceField(choices=pp_forward_choices,label='PP2 Right Wing')
        pp2ld_field = forms.ChoiceField(choices=pp_defense_choices,label='PP2 Left Defense')
        pp2rd_field = forms.ChoiceField(choices=pp_defense_choices,label='PP2 Right Defense')
        pk1c_field = forms.ChoiceField(choices=pp_defense_choices,label='PK1 Center')
        pk1w_field = forms.ChoiceField(choices=pp_defense_choices,label='PK1 Wing')
        pk1ld_field = forms.ChoiceField(choices=pp_defense_choices,label='PK1 Left Defense')
        pk1rd_field = forms.ChoiceField(choices=pp_defense_choices,label='PK1 Right Defense')
        pk2c_field = forms.ChoiceField(choices=pp_defense_choices,label='PK2 Center')
        pk2w_field = forms.ChoiceField(choices=pp_defense_choices,label='PK2 Wing')
        pk2ld_field = forms.ChoiceField(choices=pp_defense_choices,label='PK2 Left Defense')
        pk2rd_field = forms.ChoiceField(choices=pp_defense_choices,label='PK2 Right Defense')    
    return EditLinesForm

class CreatePlayerForm(forms.Form):
    position_list = ["L","C","R","D","G"]
    height_in = [66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83]
    height_ft = ["5'6","5'7","5'8","5'9","5'10","5'11","6'0","6'1","6'2","6'3","6'4","6'5","6'6","6'7","6'8","6'9","6'10","6'11"]
    weight = []
    i = 165
    while (i <= 265):
        weight.append(i)
        i += 5

    name = forms.CharField(max_length=40)
    position = forms.ChoiceField(choices=zip(position_list,position_list),label='Position')
    height = forms.ChoiceField(choices=zip(height_in,height_ft),label='Height')
    weight = forms.ChoiceField(choices=zip(weight,weight),label='Weight')
   
    def clean_name(self):
        data = self.cleaned_data['name']
        if data.strip() == "":
            raise forms.ValidationError("A name consisting of only space(s) is not a valid Player name. Please try again with a different name.")
        else:
            num_player = Player.objects.filter(name__iexact=data).count()
            if num_player == 0:
                return data
            else:
                raise forms.ValidationError("A player named '%s' already exists. Please try again with a different name."%(data))
        return data
