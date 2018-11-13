from django.contrib import messages
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import RegisterForm, LoginForm, ModifyForm, CardForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Card

import requests


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

            return HttpResponseRedirect('/tableau-de-bord/')

    else:
        form = AuthenticationForm()

    return render(request, 'files/login.html', {'form': form})


@login_required(login_url='/connexion')
def home_view(request):

    username = request.user.username
    cardsUser = Card.objects.filter(user__username=username)

    if request.method == 'POST': # logout
        logout(request)
        return HttpResponseRedirect('/')

    return render(request, 'files/home.html', {
        'cardsUser': cardsUser
    })


@login_required(login_url='/connexion')
def account_view(request):

    if request.method == 'POST': # modify user
        form_user = ModifyForm(request.POST, instance=request.user)

        if form_user.is_valid():
            form_user.save()
            return HttpResponseRedirect('/compte/')

    else:
        form_user = ModifyForm(instance=request.user)


    if request.method == 'POST': # modify password
        form_password = PasswordChangeForm(data=request.POST, user=request.user)

        if form_password.is_valid():
            user = form_password.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.INFO, 'Hello world.')
            return redirect('account')

        else:
            messages.error(request, 'Veuillez réessayer.')

    else:
        form_password = PasswordChangeForm(request.user)


    return render(request, 'files/account.html', {
        'user': request.user,
        'form_user': form_user,
        'form_password': form_password
    })


@login_required(login_url='/connexion')
def shop_view(request):

    response = requests.get('https://api.hearthstonejson.com/v1/25770/frFR/cards.collectible.json')

    cards = response.json()

    listforms = []

    for card in cards[:15]:

        if 'health' in card and 'attack' in card and 'text' in card:
            # print("Card => ",card,"\n")
            # print("Card Name => ",card['name'],"\n")

            data = {
                'name': card['name'],
                'cost': card['cost'],
                'health': card['health'],
                'attack': card['attack'],
                'text': strip_tags(card['text'])
            }

            if request.method == 'POST': # save card to user
                form = CardForm(data=request.POST, initial=data)
                listforms.append(form)

                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.user = request.user
                    instance.save()
                    return HttpResponseRedirect('/tableau-de-bord')

            else:
                form = CardForm(initial=data)
                listforms.append(form)

    return render(request, 'files/shop.html', {
        'cards': cards,
        'listforms': listforms
    })


@login_required(login_url='/connexion')
def collection_view(request):

    username = request.user.username
    cardsUser = Card.objects.filter(user__username=username)

    listforms = []
    card_action = []

    # for card in cardsUser:
    #     print('Ici la carte id => ', card.id)

    # if(request.GET.get('print_btn')):
    #     print('=> CLICK ON DEF!!!')

    # test = 6

    # if(request.GET.get('6')):
    #     print('=> CLICK ON DEF!!!')

    if(request.GET.get('sale_btn')):
        answer = request.GET
        # print('\n=> FROM SALE BTN', "\n")
        print('\n=> HERE IS ANSWER : ', answer, "\n")

    if(request.GET.get('exchange_btn')):
        print('\n=> FROM EXCHANGE BTN', "\n")

    # if(request.GET.get(str(test))):
    #     print('=> CLICK ON DEF!!!')

    # for card in cardsUser:

    #     # print('HERE IS NAME',card.name)
    #     # print('HERE IS ID',card.id)


    #     data = {
    #         'id': card.id,
    #         'name': card.name,
    #         'cost': card.cost,
    #         'health': card.health,
    #         'attack': card.attack,
    #         'text': strip_tags(card.text)
    #     }

    #     form = CardForm(initial=data)
    #     listforms.append(form)

    #     if(request.GET.get(str(card.id))):
    #         print('\n=> HERE IS MY CARDID', card.id, "\n")


    return render(request, 'files/collection.html', {
        'cardsUser': cardsUser,
        'listforms': listforms
    })
