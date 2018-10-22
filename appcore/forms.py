from django import forms
from .models import Member
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ('username', 'password')
        labels = {
            'username': 'Utilisateur',
            'password': 'Mot de passe'
        }

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {
            'username': 'Utilisateur',
            'password1': 'Mot de passe',
            'password2': 'Vérification du mot de passe'
        }

class LoginForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1')
        labels = {
            'username': 'Utilisateur',
            'password1': 'Mot de passe'
        }