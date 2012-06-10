from django import forms

class LoginForm(forms.Form):
    username_top = forms.CharField(max_length = 25)
    password_top = forms.PasswordInput()
    
