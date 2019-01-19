from django import forms
from .models import Post
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
        labels = {
            'username': 'Utilisateur',
            'password1': 'Mot de passe',
            'password2': 'Vérification du mot de passe',
            'email': 'Adresse mail'
        }

class LoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1')
        labels = {
            'username': 'Utilisateur',
            'password1': 'Mot de passe'
        }

class ModifyForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        labels = {
            'username': 'Utilisateur',
            'password': 'Mot de passe',
            'email': 'Adresse mail'
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        labels = {
            'title': 'Titre',
            'content': 'Contenu'
        }
