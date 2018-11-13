from django import forms
from .models import Card
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

class CardForm(forms.ModelForm):
    id = forms.IntegerField()

    class Meta:
        model = Card
        fields = [ 'id', 'name', 'cost', 'health', 'attack', 'text']
        labels = {
            'id': 'Identifiant',
            'name': 'Nom',
            'cost': 'Coût',
            'health': 'Santé',
            'attack': 'Attaque',
            'text': 'Propriété'
        }

    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['name'].widget.attrs['readonly'] = True

    def clean_foo_field(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            return instance.name
        else:
            return self.cleaned_data['name']
