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
        
def get_tactics_form(tactics):
    class TacticsForm(forms.Form):
        line1_time = forms.IntegerField(max_value=25,min_value=3,label="Minutes Line 1 Plays",initial=tactics.line1_time)
        line2_time = forms.IntegerField(max_value=25,min_value=3,label="Minutes Line 2 Plays",initial=tactics.line2_time)
        line3_time = forms.IntegerField(max_value=25,min_value=3,label="Minutes Line 3 Plays",initial=tactics.line3_time)
        line4_time = forms.IntegerField(max_value=25,min_value=3,label="Minutes Line 4 Plays",initial=tactics.line4_time)
        pairing1_time = forms.IntegerField(max_value=32,min_value=10,label="Minutes Pairing 1 Plays",initial=tactics.pairing1_time)
        pairing2_time = forms.IntegerField(max_value=32,min_value=10,label="Minutes Pairing 2 Plays",initial=tactics.pairing2_time)
        pairing3_time = forms.IntegerField(max_value=32,min_value=10,label="Minutes Pairing 3 Plays",initial=tactics.pairing3_time)
        match_choices = ((1,'Line 1'),(2,'Line 2'),(3,'Line 3'),(4,'Line 4'))
        home_match_line1 = forms.ChoiceField(label="Line to Use Against Opponent's Line 1",choices=match_choices,initial=tactics.match_line1)
        home_match_line2 = forms.ChoiceField(label="Line to Use Against Opponent's Line 2",choices=match_choices,initial=tactics.match_line2)
        home_match_line3 = forms.ChoiceField(label="Line to Use Against Opponent's Line 3",choices=match_choices,initial=tactics.match_line3)
        home_match_line4 = forms.ChoiceField(label="Line to Use Against Opponent's Line 4",choices=match_choices,initial=tactics.match_line4)
        match_choices = ((1,'Penalty Kill 1'),(2,'Penalty Kill 2'))
        home_match_pp1 = forms.ChoiceField(label="Penalty Kill to Use Against Opponent's Powerplay 1",choices=match_choices,initial=tactics.match_pp1)
        home_match_pp2 = forms.ChoiceField(label="Penalty Kill to Use Against Opponent's Powerplay 2",choices=match_choices,initial=tactics.match_pp2)
        match_choices = ((1,'Powerplay 1'),(2,'Powerplay 2'))
        home_match_pk1 = forms.ChoiceField(label="Powerplay to Use Against Opponent's Penalty Kill 1",choices=match_choices,initial=tactics.match_pk1)
        home_match_pk2 = forms.ChoiceField(label="Powerplay to Use Against Opponent's Penalty Kill 2",choices=match_choices,initial=tactics.match_pk2)
        
        def clean(self):
            cleaned_data = super(TacticsForm,self).clean()
            try:
                line4_time = int(self.cleaned_data.get('line4_time'))
                line1_time = int(self.cleaned_data.get('line1_time'))
                line2_time = int(self.cleaned_data.get('line2_time'))
                line3_time = int(self.cleaned_data.get('line3_time'))
                temp = line1_time + line2_time + line3_time + line4_time
                if temp != 60:
                    raise forms.ValidationError("Line 1 icetime, Line 2 icetime, Line 3 icetime, and line 4 icetime must add up to exactly 60. Line 1 icetime + Line 2 icetime + Line 3 icetime + Line 4 icetime currently equals %s, which does not equal 60." %(temp))
            except (NameError,TypeError):
                pass
            try:
                pairing1_time = int(cleaned_data.get('pairing1_time'))
                pairing2_time = int(cleaned_data.get('pairing2_time'))
                pairing3_time = int(cleaned_data.get('pairing3_time'))
                temp = pairing1_time + pairing2_time + pairing3_time 
                if temp != 60:
                    raise forms.ValidationError("Pairing 1 icetime,Pairing 2 icetime, and Pairing 3 icetime must add up to exactly 60. Pairing 1 icetime + Pairing 2 icetime + Pairing 3 icetime currently equals %s, which does not equal 60." % (temp))          
            except (NameError,TypeError):
                pass
            try:
                lines_matched = []
                home_match1 =int(cleaned_data.get('home_match_line1'))
                home_match2 =int(cleaned_data.get('home_match_line2'))
                home_match3 =int(cleaned_data.get('home_match_line3'))
                home_match4 =int(cleaned_data.get('home_match_line4'))
                lines_matched.append(home_match1)
                if home_match2 in lines_matched:
                    raise forms.ValidationError("Line %s is used to match more than one of the opponent's lines" % (home_match2))
                lines_matched.append(home_match2)
                if home_match3 in lines_matched:
                    raise forms.ValidationError("Line %s is used to match more than one of the opponent's lines" % (home_match3))
                lines_matched.append(home_match3)
                if home_match4 in lines_matched:
                    raise forms.ValidationError("Line %s is used to match more than one of the opponent's lines" % (home_match4))
            except (NameError,TypeError):
                pass
            try:
                home_matchpp1 =int(cleaned_data.get('home_match_pp1'))
                home_matchpp2 =int(cleaned_data.get('home_match_pp2'))
                if home_matchpp1 == home_matchpp2:
                    raise forms.ValidationError("Penalty kill unit %s is used to match both of the opponent's powerplays. Please use your other penalty kill unit to match one of the opponent's powerplays." % (home_matchpp1))
            except (NameError,TypeError):
                pass
            try:
                home_matchpk1 =int(cleaned_data.get('home_match_pk1'))
                home_matchpk2 =int(cleaned_data.get('home_match_pk2'))
                if home_matchpk1 == home_matchpk2:
                    raise forms.ValidationError("Powerplay unit %s is used to match both of the opponent's penalty kills. Please use your other powerplay unit to match one of the opponent's penalty kills." % (home_matchpk1))       
            except (NameError,TypeError):
                pass
            return cleaned_data
    return TacticsForm


      
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
            l1_field = forms.ChoiceField(choices=l_choices,initial=team.lw1,label='Line 1 Left Wing')
        else:
            l1_field = forms.ChoiceField(choices=l_choices,label='Line 1 Left Wing')
        if player_list.filter(pk=team.c1).count() == 1:
            c1_field = forms.ChoiceField(choices=c_choices,initial=team.c1,label='Line 1 Center')
        else:
            c1_field = forms.ChoiceField(choices=c_choices,label='Line 1 Center')
        if player_list.filter(pk=team.rw1).count() == 1:
            r1_field = forms.ChoiceField(choices=r_choices,initial=team.rw1,label='Line 1 Right Wing')
        else:
            r1_field = forms.ChoiceField(choices=r_choices,label='Line 1 Right Wing')
        if player_list.filter(pk=team.defense1).count() == 1:
            d1_field = forms.ChoiceField(choices=d_choices,initial=team.defense1,label='Pairing 1 Left Defense')
        else:
            d1_field = forms.ChoiceField(choices=d_choices,label='Pairing 1 Left Defense')
        if player_list.filter(pk=team.goalie1).count() == 1:
            g1_field = forms.ChoiceField(choices=g_choices,initial=team.goalie1,label='Starting Goalie')
        else:
            g1_field = forms.ChoiceField(choices=g_choices,label='Starting Goalie')
        if player_list.filter(pk=team.lw2).count() == 1:
            l2_field = forms.ChoiceField(choices=l_choices,initial=team.lw2,label='Line 2 Left Wing')
        else:
            l2_field = forms.ChoiceField(choices=l_choices,label='Line 2 Left Wing')
        if player_list.filter(pk=team.c2).count() == 1:
            c2_field = forms.ChoiceField(choices=c_choices,initial=team.c2,label='Line 2 Center')
        else:
            c2_field = forms.ChoiceField(choices=c_choices,label='Line 2 Center')
        if player_list.filter(pk=team.rw2).count() == 1:
            r2_field = forms.ChoiceField(choices=r_choices,initial=team.rw2,label='Line 2 Right Wing')
        else:
            r2_field = forms.ChoiceField(choices=r_choices,label='Line 2 Right Wing')
        if player_list.filter(pk=team.defense2).count() == 1:
            d2_field = forms.ChoiceField(choices=d_choices,initial=team.defense2,label='Pairing 1 Right Defense')
        else:
            d2_field = forms.ChoiceField(choices=d_choices,label='Pairing 1 Right Defense')
        if player_list.filter(pk=team.goalie2).count() == 1:
            g2_field = forms.ChoiceField(choices=g_choices,initial=team.goalie2,label='Backup Goalie')
        else:
            g2_field = forms.ChoiceField(choices=g_choices,label='Backup Goalie')
        if player_list.filter(pk=team.lw3).count() == 1:
            l3_field = forms.ChoiceField(choices=l_choices,initial=team.lw3,label='Line 3 Left Wing')
        else:
            l3_field = forms.ChoiceField(choices=l_choices,label='Line 3 Left Wing')
        if player_list.filter(pk=team.c3).count() == 1:
            c3_field = forms.ChoiceField(choices=c_choices,initial=team.c3,label='Line 3 Center')
        else:
            c3_field = forms.ChoiceField(choices=c_choices,label='Line 3 Center')
        if player_list.filter(pk=team.rw3).count() == 1:
            r3_field = forms.ChoiceField(choices=r_choices,initial=team.rw3,label='Line 3 Right Wing')
        else:
            r3_field = forms.ChoiceField(choices=r_choices,label='Line 3 Right Wing')
        if player_list.filter(pk=team.defense3).count() == 1:
            d3_field = forms.ChoiceField(choices=d_choices,initial=team.defense3,label='Pairing 2 Left Defense')
        else:
            d3_field = forms.ChoiceField(choices=d_choices,label='Pairing 2 Left Defense')
        if player_list.filter(pk=team.lw4).count() == 1:
            l4_field = forms.ChoiceField(choices=l_choices,initial=team.lw4,label='Line 4 Left Wing')
        else:
            l4_field = forms.ChoiceField(choices=l_choices,label='Line 4 Left Wing')
        if player_list.filter(pk=team.c4).count() == 1:
            c4_field = forms.ChoiceField(choices=c_choices,initial=team.c4,label='Line 4 Center')
        else:
            c4_field = forms.ChoiceField(choices=c_choices,label='Line 4 Center')
        if player_list.filter(pk=team.rw4).count() == 1:
            r4_field = forms.ChoiceField(choices=r_choices,initial=team.rw4,label='Line 4 Right Wing')
        else:
            r4_field = forms.ChoiceField(choices=r_choices,label='Line 4 Right Wing')
        if player_list.filter(pk=team.defense4).count() == 1:
            d4_field = forms.ChoiceField(choices=d_choices,initial=team.defense4,label='Pairing 2 Right Defense')
        else:
            d4_field = forms.ChoiceField(choices=d_choices,label='Pairing 2 Right Defense')
        if player_list.filter(pk=team.defense5).count() == 1:
            d5_field = forms.ChoiceField(choices=d_choices,initial=team.defense5,label='Pairing 3 Left Defense')
        else:
            d5_field = forms.ChoiceField(choices=d_choices,label='Pairing 3 Left Defense')
        if player_list.filter(pk=team.defense6).count() == 1:
            d6_field = forms.ChoiceField(choices=d_choices,initial=team.defense6,label='Pairing 3 Right Defense')
        else:
            d6_field = forms.ChoiceField(choices=d_choices,label='Pairing 3 Right Defense')
        if player_list.filter(pk=team.pp1lw).count() == 1:
            pp1l_field = forms.ChoiceField(choices=pp_forward_choices,initial=team.pp1lw,label='PP1 Left Wing')
        else:
            pp1l_field = forms.ChoiceField(choices=pp_forward_choices,label='PP1 Left Wing')
        if player_list.filter(pk=team.pp1c).count() == 1:
            pp1c_field = forms.ChoiceField(choices=pp_forward_choices,initial=team.pp1c,label='PP1 Center')
        else:
            pp1c_field = forms.ChoiceField(choices=pp_forward_choices,label='PP1 Center')
        if player_list.filter(pk=team.pp1rw).count() == 1:
            pp1r_field = forms.ChoiceField(choices=pp_forward_choices,initial=team.pp1rw,label='PP1 Right Wing')
        else:
            pp1r_field = forms.ChoiceField(choices=pp_forward_choices,label='PP1 Right Wing')
        if player_list.filter(pk=team.pp1ld).count() == 1:
            pp1ld_field = forms.ChoiceField(choices=pp_defense_choices,initial=team.pp1ld,label='PP1 Left Defense')
        else:
            pp1ld_field = forms.ChoiceField(choices=pp_defense_choices,label='PP1 Left Defense')
        if player_list.filter(pk=team.pp1rd).count() == 1:
            pp1rd_field = forms.ChoiceField(choices=pp_defense_choices,initial=team.pp1rd,label='PP1 Right Defense')
        else:
            pp1rd_field = forms.ChoiceField(choices=pp_defense_choices,label='PP1 Right Defense')
        if player_list.filter(pk=team.pp2lw).count() == 1:
            pp2l_field = forms.ChoiceField(choices=pp_forward_choices,initial=team.pp2lw,label='PP2 Left Wing')
        else:
            pp2l_field = forms.ChoiceField(choices=pp_forward_choices,label='PP2 Left Wing')
        if player_list.filter(pk=team.pp2c).count() == 1:
            pp2c_field = forms.ChoiceField(choices=pp_forward_choices,initial=team.pp2c,label='PP2 Center')
        else:
            pp2c_field = forms.ChoiceField(choices=pp_forward_choices,label='PP2 Center')
        if player_list.filter(pk=team.pp2rw).count() == 1:
            pp2r_field = forms.ChoiceField(choices=pp_forward_choices,initial=team.pp2rw,label='PP2 Right Wing')
        else:
            pp2r_field = forms.ChoiceField(choices=pp_forward_choices,label='PP2 Right Wing')
        if player_list.filter(pk=team.pp2ld).count() == 1:
            pp2ld_field = forms.ChoiceField(choices=pp_defense_choices,initial=team.pp2ld,label='PP2 Left Defense')
        else:
            pp2ld_field = forms.ChoiceField(choices=pp_defense_choices,label='PP2 Left Defense')
        if player_list.filter(pk=team.pp2rd).count() == 1:
            pp2rd_field = forms.ChoiceField(choices=pp_defense_choices,initial=team.pp2rd,label='PP2 Right Defense')
        else:
            pp2rd_field = forms.ChoiceField(choices=pp_defense_choices,label='PP2 Right Defense')
        if player_list.filter(pk=team.pk1c).count() == 1:
            pk1c_field = forms.ChoiceField(choices=pp_defense_choices,initial=team.pk1c,label='PK1 Center')
        else:
            pk1c_field = forms.ChoiceField(choices=pp_defense_choices,label='PK1 Center')
        if player_list.filter(pk=team.pk1w).count() == 1:
            pk1w_field = forms.ChoiceField(choices=pp_defense_choices,initial=team.pk1w,label='PK1 Wing')
        else:
            pk1w_field = forms.ChoiceField(choices=pp_defense_choices,label='PK1 Wing')
        if player_list.filter(pk=team.pk1ld).count() == 1:
            pk1ld_field = forms.ChoiceField(choices=pp_defense_choices,initial=team.pk1ld,label='PK1 Left Defense')
        else:
            pk1ld_field = forms.ChoiceField(choices=pp_defense_choices,label='PK1 Left Defense')
        if player_list.filter(pk=team.pk1rd).count() == 1:
            pk1rd_field = forms.ChoiceField(choices=pp_defense_choices,initial=team.pk1rd,label='PK1 Right Defense')
        else:
            pk1rd_field = forms.ChoiceField(choices=pp_defense_choices,label='PK1 Right Defense')
        if player_list.filter(pk=team.pk2c).count() == 1:
            pk2c_field = forms.ChoiceField(choices=pp_defense_choices,initial=team.pk2c,label='PK2 Center')
        else:
            pk2c_field = forms.ChoiceField(choices=pp_defense_choices,label='PK2 Center')
        if player_list.filter(pk=team.pk2w).count() == 1:
            pk2w_field = forms.ChoiceField(choices=pp_defense_choices,initial=team.pk2w,label='PK2 Wing')
        else:
            pk2w_field = forms.ChoiceField(choices=pp_defense_choices,label='PK2 Wing')
        if player_list.filter(pk=team.pk2ld).count() == 1:
            pk2ld_field = forms.ChoiceField(choices=pp_defense_choices,initial=team.pk2ld,label='PK2 Left Defense')
        else:
            pk2ld_field = forms.ChoiceField(choices=pp_defense_choices,label='PK2 Left Defense')
        if player_list.filter(pk=team.pk2rd).count() == 1:
            pk2rd_field = forms.ChoiceField(choices=pp_defense_choices,initial=team.pk2rd,label='PK2 Right Defense')
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
