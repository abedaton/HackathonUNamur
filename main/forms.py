from django import forms

class LoginForm(forms.Form):
    mail = forms.EmailField()
    password = forms.CharField()

