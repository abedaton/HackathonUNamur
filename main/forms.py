from django import forms

class LoginForm(forms.Form):
    mail = forms.EmailField()
    mail.widget = forms.TextInput(attrs={"class":"form-control", "id":"InputEmail1", "aria-describedby":"emailHelp", "placeholder":"Entrez votre adresse e-mail"})
    password = forms.CharField(widget=forms.PasswordInput)
    password.widget = forms.TextInput(attrs={"class": "form-control", "id": "exampleInputPassword1", "placeholder": "Entrez votre mot de passe"})

