from django import forms

class TeamForm(forms.Form):
    name = forms.CharField(max_length=40)
    abbreviation = forms.CharField(max_length=3, min_length=2)
    arena_name = forms.CharField(max_length=40)


class OfferPlayerContractForm(forms.Form):
    salary = forms.IntegerField(max_value=20000000, min_value=50000, label="Salary Per Year (Integer between 50000 and 20000000)",widget=forms.TextInput(attrs={'class':'span2'}))
    length = forms.IntegerField(max_value=10, min_value=1, label="Length of the Contract (Integer between 1 and 10)",widget=forms.TextInput(attrs={'class':'span1'}))
    no_trade = forms.BooleanField(required=False)
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
        l1_field = forms.ChoiceField(choices=l_choices,label='Line 1 L')
        c1_field = forms.ChoiceField(choices=c_choices,label='Line 1 C')
        r1_field = forms.ChoiceField(choices=r_choices,label='Line 1 R')
        d1_field = forms.ChoiceField(choices=d_choices,label='Pairing 1 ')
        g1_field = forms.ChoiceField(choices=g_choices,label='Starting Goalie')
        l2_field = forms.ChoiceField(choices=l_choices,label='Line 2 L')
        c2_field = forms.ChoiceField(choices=c_choices,label='Line 2 C')
        r2_field = forms.ChoiceField(choices=r_choices,label='Line 2 R')
        d2_field = forms.ChoiceField(choices=d_choices,label='Pairing 1')
        g2_field = forms.ChoiceField(choices=g_choices,label='Backup Goalie')
        l3_field = forms.ChoiceField(choices=l_choices,label='Line 3 L')
        c3_field = forms.ChoiceField(choices=c_choices,label='Line 3 C')
        r3_field = forms.ChoiceField(choices=r_choices,label='Line 3 R')
        d3_field = forms.ChoiceField(choices=d_choices,label='Pairing 2')
        l4_field = forms.ChoiceField(choices=l_choices,label='Line 4 L')
        c4_field = forms.ChoiceField(choices=c_choices,label='Line 4 C')
        r4_field = forms.ChoiceField(choices=r_choices,label='Line 4 R')
        d4_field = forms.ChoiceField(choices=d_choices,label='Pairing 2')
        d5_field = forms.ChoiceField(choices=d_choices,label='Pairing 3')
        d6_field = forms.ChoiceField(choices=d_choices,label='Pairing 3')
    return EditLinesForm



