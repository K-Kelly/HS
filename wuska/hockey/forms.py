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
        
        
def make_edit_lines_form(team):
    class EditLinesForm(forms.Form):
        player_list = team.players
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
        
        if player_list.filter(pk=team.lw1).count() == 1:
            l1_field = forms.ChoiceField(choices=l_choices,initial={team.lw1:player_list.filter(pk=team.lw1)[0].name},label='Line 1 Left Wing')
        else:
            l1_field = forms.ChoiceField(choices=l_choices,label='Line 1 Left Wing')
        if player_list.filter(pk=team.c1).count() == 1:
            c1_field = forms.ChoiceField(choices=c_choices,initial={team.c1:player_list.filter(pk=team.c1)[0].name},label='Line 1 Center')
        else:
            c1_field = forms.ChoiceField(choices=c_choices,label='Line 1 Center')
        if player_list.filter(pk=team.rw1).count() == 1:
            r1_field = forms.ChoiceField(choices=r_choices,initial={team.rw1:player_list.filter(pk=team.rw1)[0].name},label='Line 1 Right Wing')
        else:
            r1_field = forms.ChoiceField(choices=r_choices,label='Line 1 Right Wing')
        if player_list.filter(pk=team.defense1).count() == 1:
            d1_field = forms.ChoiceField(choices=d_choices,initial={team.defense1:player_list.filter(pk=team.defense1)[0].name},label='Pairing 1 Left Defense')
        else:
            d1_field = forms.ChoiceField(choices=d_choices,label='Pairing 1 Left Defense')
        if player_list.filter(pk=team.goalie1).count() == 1:
            g1_field = forms.ChoiceField(choices=g_choices,initial={team.goalie1:player_list.filter(pk=team.goalie1)[0].name},label='Starting Goalie')
        else:
            g1_field = forms.ChoiceField(choices=g_choices,label='Starting Goalie')
        if player_list.filter(pk=team.lw2).count() == 1:
            l2_field = forms.ChoiceField(choices=l_choices,initial={team.lw2:player_list.filter(pk=team.lw2)[0].name},label='Line 2 Left Wing')
        else:
            l2_field = forms.ChoiceField(choices=l_choices,label='Line 2 Left Wing')
        if player_list.filter(pk=team.c2).count() == 1:
            c2_field = forms.ChoiceField(choices=c_choices,initial={team.c2:player_list.filter(pk=team.c2)[0].name},label='Line 2 Center')
        else:
            c2_field = forms.ChoiceField(choices=c_choices,label='Line 2 Center')
        if player_list.filter(pk=team.rw2).count() == 1:
            r2_field = forms.ChoiceField(choices=r_choices,initial={team.rw2:player_list.filter(pk=team.rw2)[0].name},label='Line 2 Right Wing')
        else:
            r2_field = forms.ChoiceField(choices=r_choices,label='Line 2 Right Wing')
        if player_list.filter(pk=team.defense2).count() == 1:
            d2_field = forms.ChoiceField(choices=d_choices,initial={team.defense2:player_list.filter(pk=team.defense2)[0].name},label='Pairing 1 Right Defense')
        else:
            d2_field = forms.ChoiceField(choices=d_choices,label='Pairing 1 Right Defense')
        if player_list.filter(pk=team.goalie2).count() == 1:
            g2_field = forms.ChoiceField(choices=g_choices,initial={team.goalie2:player_list.filter(pk=team.goalie2)[0].name},label='Backup Goalie')
        else:
            g2_field = forms.ChoiceField(choices=g_choices,label='Backup Goalie')
        if player_list.filter(pk=team.lw3).count() == 1:
            l3_field = forms.ChoiceField(choices=l_choices,initial={team.lw3:player_list.filter(pk=team.lw3)[0].name},label='Line 3 Left Wing')
        else:
            l3_field = forms.ChoiceField(choices=l_choices,label='Line 3 Left Wing')
        if player_list.filter(pk=team.c3).count() == 1:
            c3_field = forms.ChoiceField(choices=c_choices,initial={team.c3:player_list.filter(pk=team.c3)[0].name},label='Line 3 Center')
        else:
            c3_field = forms.ChoiceField(choices=c_choices,label='Line 3 Center')
        if player_list.filter(pk=team.rw3).count() == 1:
            r3_field = forms.ChoiceField(choices=r_choices,initial={team.rw3:player_list.filter(pk=team.rw3)[0].name},label='Line 3 Right Wing')
        else:
            r3_field = forms.ChoiceField(choices=r_choices,label='Line 3 Right Wing')
        if player_list.filter(pk=team.defense3).count() == 1:
            d3_field = forms.ChoiceField(choices=d_choices,initial={team.defense3:player_list.filter(pk=team.defense3)[0].name},label='Pairing 2 Left Defense')
        else:
            d3_field = forms.ChoiceField(choices=d_choices,label='Pairing 2 Left Defense')
        if player_list.filter(pk=team.lw4).count() == 1:
            l4_field = forms.ChoiceField(choices=l_choices,initial={team.lw4:player_list.filter(pk=team.lw4)[0].name},label='Line 4 Left Wing')
        else:
            l4_field = forms.ChoiceField(choices=l_choices,label='Line 4 Left Wing')
        if player_list.filter(pk=team.c4).count() == 1:
            c4_field = forms.ChoiceField(choices=c_choices,initial={team.c4:player_list.filter(pk=team.c4)[0].name},label='Line 4 Center')
        else:
            c4_field = forms.ChoiceField(choices=c_choices,label='Line 4 Center')
        if player_list.filter(pk=team.rw4).count() == 1:
            r4_field = forms.ChoiceField(choices=r_choices,initial={team.rw4:player_list.filter(pk=team.rw4)[0].name},label='Line 4 Right Wing')
        else:
            r4_field = forms.ChoiceField(choices=r_choices,label='Line 4 Right Wing')
        if player_list.filter(pk=team.defense4).count() == 1:
            d4_field = forms.ChoiceField(choices=d_choices,initial={team.defense4:player_list.filter(pk=team.defense4)[0].name},label='Pairing 2 Right Defense')
        else:
            d4_field = forms.ChoiceField(choices=d_choices,label='Pairing 2 Right Defense')
        if player_list.filter(pk=team.defense5).count() == 1:
            d5_field = forms.ChoiceField(choices=d_choices,initial={team.defense5:player_list.filter(pk=team.defense5)[0].name},label='Pairing 3 Left Defense')
        else:
            d5_field = forms.ChoiceField(choices=d_choices,label='Pairing 3 Left Defense')
        if player_list.filter(pk=team.defense6).count() == 1:
            d6_field = forms.ChoiceField(choices=d_choices,initial={team.defense6:player_list.filter(pk=team.defense6)[0].name},label='Pairing 3 Right Defense')
        else:
            d6_field = forms.ChoiceField(choices=d_choices,label='Pairing 3 Right Defense')
        if player_list.filter(pk=team.pp1lw).count() == 1:
            pp1l_field = forms.ChoiceField(choices=pp_forward_choices,initial={team.pp1lw:player_list.filter(pk=team.pp1lw)[0].name},label='PP1 Left Wing')
        else:
            pp1l_field = forms.ChoiceField(choices=pp_forward_choices,label='PP1 Left Wing')
        if player_list.filter(pk=team.pp1c).count() == 1:
            pp1c_field = forms.ChoiceField(choices=pp_forward_choices,initial={team.pp1c:player_list.filter(pk=team.pp1c)[0].name},label='PP1 Center')
        else:
            pp1c_field = forms.ChoiceField(choices=pp_forward_choices,label='PP1 Center')
        if player_list.filter(pk=team.pp1rw).count() == 1:
            pp1r_field = forms.ChoiceField(choices=pp_forward_choices,initial={team.pp1rw:player_list.filter(pk=team.pp1rw)[0].name},label='PP1 Right Wing')
        else:
            pp1r_field = forms.ChoiceField(choices=pp_forward_choices,label='PP1 Right Wing')
        if player_list.filter(pk=team.pp1ld).count() == 1:
            pp1ld_field = forms.ChoiceField(choices=pp_defense_choices,initial={team.pp1ld:player_list.filter(pk=team.pp1ld)[0].name},label='PP1 Left Defense')
        else:
            pp1ld_field = forms.ChoiceField(choices=pp_defense_choices,label='PP1 Left Defense')
        if player_list.filter(pk=team.pp1rd).count() == 1:
            pp1rd_field = forms.ChoiceField(choices=pp_defense_choices,initial={team.pp1rd:player_list.filter(pk=team.pp1rd)[0].name},label='PP1 Right Defense')
        else:
            pp1rd_field = forms.ChoiceField(choices=pp_defense_choices,label='PP1 Right Defense')
        if player_list.filter(pk=team.pp2lw).count() == 1:
            pp2l_field = forms.ChoiceField(choices=pp_forward_choices,initial={team.pp2lw:player_list.filter(pk=team.pp2lw)[0].name},label='PP2 Left Wing')
        else:
            pp2l_field = forms.ChoiceField(choices=pp_forward_choices,label='PP2 Left Wing')
        if player_list.filter(pk=team.pp2c).count() == 1:
            pp2c_field = forms.ChoiceField(choices=pp_forward_choices,initial={team.pp2c:player_list.filter(pk=team.pp2c)[0].name},label='PP2 Center')
        else:
            pp2c_field = forms.ChoiceField(choices=pp_forward_choices,label='PP2 Center')
        if player_list.filter(pk=team.pp2rw).count() == 1:
            pp2r_field = forms.ChoiceField(choices=pp_forward_choices,initial={team.pp2rw:player_list.filter(pk=team.pp2rw)[0].name},label='PP2 Right Wing')
        else:
            pp2r_field = forms.ChoiceField(choices=pp_forward_choices,label='PP2 Right Wing')
        if player_list.filter(pk=team.pp2ld).count() == 1:
            pp2ld_field = forms.ChoiceField(choices=pp_defense_choices,initial={team.pp2ld:player_list.filter(pk=team.pp2ld)[0].name},label='PP2 Left Defense')
        else:
            pp2ld_field = forms.ChoiceField(choices=pp_defense_choices,label='PP2 Left Defense')
        if player_list.filter(pk=team.pp2rd).count() == 1:
            pp2rd_field = forms.ChoiceField(choices=pp_defense_choices,initial={team.pp2rd:player_list.filter(pk=team.pp2rd)[0].name},label='PP2 Right Defense')
        else:
            pp2rd_field = forms.ChoiceField(choices=pp_defense_choices,label='PP2 Right Defense')
        if player_list.filter(pk=team.pk1c).count() == 1:
            pk1c_field = forms.ChoiceField(choices=pp_defense_choices,initial={team.pk1c:player_list.filter(pk=team.pk1c)[0].name},label='PK1 Center')
        else:
            pk1c_field = forms.ChoiceField(choices=pp_defense_choices,label='PK1 Center')
        if player_list.filter(pk=team.pk1w).count() == 1:
            pk1w_field = forms.ChoiceField(choices=pp_defense_choices,initial={team.pk1w:player_list.filter(pk=team.pk1w)[0].name},label='PK1 Wing')
        else:
            pk1w_field = forms.ChoiceField(choices=pp_defense_choices,label='PK1 Wing')
        if player_list.filter(pk=team.pk1ld).count() == 1:
            pk1ld_field = forms.ChoiceField(choices=pp_defense_choices,initial={team.pk1ld:player_list.filter(pk=team.pk1ld)[0].name},label='PK1 Left Defense')
        else:
            pk1ld_field = forms.ChoiceField(choices=pp_defense_choices,label='PK1 Left Defense')
        if player_list.filter(pk=team.pk1rd).count() == 1:
            pk1rd_field = forms.ChoiceField(choices=pp_defense_choices,initial={team.pk1rd:player_list.filter(pk=team.pk1rd)[0].name},label='PK1 Right Defense')
        else:
            pk1rd_field = forms.ChoiceField(choices=pp_defense_choices,label='PK1 Right Defense')
        if player_list.filter(pk=team.pk2c).count() == 1:
            pk2c_field = forms.ChoiceField(choices=pp_defense_choices,initial={team.pk2c:player_list.filter(pk=team.pk2c)[0].name},label='PK2 Center')
        else:
            pk2c_field = forms.ChoiceField(choices=pp_defense_choices,label='PK2 Center')
        if player_list.filter(pk=team.pk2w).count() == 1:
            pk2w_field = forms.ChoiceField(choices=pp_defense_choices,initial={team.pk2w:player_list.filter(pk=team.pk2w)[0].name},label='PK2 Wing')
        else:
            pk2w_field = forms.ChoiceField(choices=pp_defense_choices,label='PK2 Wing')
        if player_list.filter(pk=team.pk2ld).count() == 1:
            pk2ld_field = forms.ChoiceField(choices=pp_defense_choices,initial={team.pk2ld:player_list.filter(pk=team.pk2ld)[0].name},label='PK2 Left Defense')
        else:
            pk2ld_field = forms.ChoiceField(choices=pp_defense_choices,label='PK2 Left Defense')
        if player_list.filter(pk=team.pk2rd).count() == 1:
            pk2rd_field = forms.ChoiceField(choices=pp_defense_choices,initial={team.pk2rd:player_list.filter(pk=team.pk2rd)[0].name},label='PK2 Right Defense')
        else:
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
