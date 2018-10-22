from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required


def welcome_view(request):
    return render(request, 'files/welcome.html')


def register_view(request):

    if request.method == 'POST': # register
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/connexion/')

    else:
        form = RegisterForm()

    return render(request, 'files/register.html', {'form': form})


def login_view(request):

    if request.method == 'POST': # login
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return HttpResponseRedirect('/accueil/')

    else:
        form = AuthenticationForm()

    return render(request, 'files/login.html', {'form': form})

@login_required(login_url='/connexion')
def home_view(request):

    if request.method == 'POST': # logout
        logout(request)
        return HttpResponseRedirect('/')

    return render(request, 'files/home.html')

