from django import forms


class LoginForm(forms.Form):
    loginClass = forms.TextInput(attrs={"class": "form-control"})
    passwordClass = forms.PasswordInput(attrs={"class": "form-control"})
    login = forms.CharField(widget=loginClass, label="Login:", max_length=50, required=True)
    password = forms.CharField(widget=passwordClass, label="Hasło:", max_length=50, required=True)


class RegisterForm(forms.Form):
    loginClass = forms.TextInput(attrs={"class": "form-control"})
    passwordClass = forms.PasswordInput(attrs={"class": "form-control"})
    login = forms.CharField(widget=loginClass, label="Login:", max_length=50, required=True)
    email = forms.CharField(widget=loginClass, label="Email:", max_length=50, required=True)
    password = forms.CharField(widget=passwordClass, label="Hasło:", max_length=50, required=True)


class ServerForm(forms.Form):
    textClass = forms.TextInput(attrs={"class": "form-control"})
    intClass = forms.NumberInput(attrs={"class": "form-control"})
    name = forms.CharField(widget=textClass, label="Nazwa gry:", max_length=100, required=True)
    max_players = forms.IntegerField(widget=intClass, label="Maksymalna liczba graczy:", required=True)
    rounds = forms.IntegerField(widget=intClass, label="Liczba rund:", required=True)
