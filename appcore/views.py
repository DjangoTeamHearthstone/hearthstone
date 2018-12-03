from django.contrib import messages
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import RegisterForm, LoginForm, ModifyForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Card, Deck, User_Card, Deck_Card, Profile, Post, Exchange, Exchange_Card
from django.template.defaulttags import register
from django.conf.urls.static import static
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import datetime, requests, random, os, json


# Global functions #
def activate_paginator(request, cards, nb):
    paginator = Paginator(cards, nb)
    page = request.GET.get('page')
    return paginator.get_page(page)

def random_name_deck():
    default_name_deck = [
        'Deck des Arcanes', 'Deck des Sombres Puissances', 'Deck Magus de Dalaran',
        'Deck du Secret Eternel', 'Deck Amazone', 'Deck Trépas de Doomhammer',
        'Deck Loup de Givre', 'Deck de Bric et de Brac', 'Deck Sombrelance',
        'Deck Main de Fer', 'Deck de Teldrassil', 'Deck de l\'Ordre d\'Argent',
        'Deck du Néant', 'Deck Rage Animale', 'Deck Déferlante de Feu',
        'Deck des Ewoks Déchaînés', 'Deck de la Légion', 'Deck Croisade Ecarlate'
    ]
    return random.choice(default_name_deck)

# Views functions #
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

            return HttpResponseRedirect('/tableau-de-bord')

    else:
        form = AuthenticationForm()

    return render(request, 'files/login.html', {'form': form})


@login_required(login_url='/connexion')
def home_view(request):

    zipped = []
    exchanges = []
    list_creators = []
    list_id_exchange = []
    list_l_cards_creator = []
    list_l_cards_assignee = []

    if Exchange.objects.filter(assignee=request.user).count():
        exchanges = Exchange.objects.filter(assignee=request.user)
        for exchange in exchanges:
            list_cards_creator = []
            list_cards_assignee = []
            list_creators.append(exchange.creator)
            list_id_exchange.append(exchange.id)
            card_exchanges_creator = exchange.exchange_card.filter(creator_assignee=0)
            card_exchanges_assignee = exchange.exchange_card.filter(creator_assignee=1)
            for card_exchange in card_exchanges_creator:
                list_cards_creator.append(card_exchange.card_key)
            for card_exchange in card_exchanges_assignee:
                list_cards_assignee.append(card_exchange.card_key)
            list_l_cards_creator.append(list_cards_creator)
            list_l_cards_assignee.append(list_cards_assignee)
        zipped = list(zip(list_creators, list_l_cards_creator, list_l_cards_assignee, list_id_exchange))

    if request.POST.get('accept_btn'): # accept exchange
        exchange_accepted = Exchange.objects.get(id=request.POST.get('accept_btn'))
        assignee = request.user
        creator = exchange_accepted.creator
        print('\nHERE IS CREATOR => ',creator,'\n')
        list_cards_creator = []
        list_cards_assignee = []

        card_exchanges_creator = exchange_accepted.exchange_card.filter(creator_assignee=0)
        card_exchanges_assignee = exchange_accepted.exchange_card.filter(creator_assignee=1)
        for card_exchange in card_exchanges_creator:
            User_Card(user_key=assignee,card_key=card_exchange.card_key).save()
            # print('\nHERE IS CREATOR => ',creator,'\n')
            # print('\nHERE IS CARD KEY => ',card_exchange.card_key,'\n')
            # print('\nHERE IS RELATION => ',User_Card.objects.filter(user_key=creator,card_key=card_exchange.card_key),'\n')
            User_Card.objects.filter(user_key=creator,card_key=card_exchange.card_key).delete()
        for card_exchange in card_exchanges_assignee:
            User_Card(user_key=creator,card_key=card_exchange.card_key).save()
            User_Card.objects.filter(user_key=assignee,card_key=card_exchange.card_key).delete()

        exchange_accepted.delete()
        return HttpResponseRedirect('/tableau-de-bord')

    if request.POST.get('refuse_btn'): # refuse exchange
        exchange_refused = Exchange.objects.get(id=int(request.POST.get('refuse_btn')))
        exchange_refused.delete()
        return HttpResponseRedirect('/tableau-de-bord')
    # exchange_received_id = []

    # exchanges_received = Exchange.objects.filter(assignee__username=request.user.username)
    # [ exchange_received_id.append(exchanges_received.values()[c].get('id'))
    #     for c, x in enumerate(exchanges_received)]
    # for exchange in exchanges_received:
    #     list_creators.append(User.objects.get(id=exchange.creator_id))
    #     list_l_cards_creator.append(preparing_list_exchange(request, exchange.cards_creator))
    #     list_l_cards_assignee.append(preparing_list_exchange(request, exchange.cards_assignee))
    # zipped = list(zip(list_creators, list_l_cards_creator, list_l_cards_assignee, exchange_received_id))

    # if(request.GET.get('accept_btn')): # accept exchange
    #     data = request.GET
    #     exchange_accepted = Exchange.objects.get(id=data.get('accept_btn'))
    #     [Card.objects.filter(id=card).update(user=exchange_accepted.assignee)
    #         for card in exchange_accepted.cards_creator]
    #     [Card.objects.filter(id=card).update(user=exchange_accepted.creator)
    #         for card in exchange_accepted.cards_assignee]
    #     exchange_accepted.delete()
    #     return HttpResponseRedirect('/tableau-de-bord')

    # if(request.GET.get('refuse_btn')): # refuse exchange
    #     data = request.GET
    #     exchange_refused = Exchange.objects.get(id=data.get('refuse_btn'))
    #     exchange_refused.delete()
    #     return HttpResponseRedirect('/tableau-de-bord')

    if (request.POST.get('logout_btn')): # logout
        logout(request)
        return HttpResponseRedirect('/')


    return render(request, 'files/home.html', {
        'exchanges': exchanges,
        'zipped': zipped
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
            return HttpResponseRedirect('/compte/')

        else:
            return HttpResponseRedirect('/compte/')

    else:
        form_password = PasswordChangeForm(request.user)
        form_password.fields['old_password'].label = 'Ancien mot de passe'
        form_password.fields['new_password1'].label = 'Nouveau mot de passe'
        form_password.fields['new_password2'].label = 'Confirmer mot de passe'


    return render(request, 'files/account.html', {
        'user': request.user,
        'form_user': form_user,
        'form_password': form_password
    })


@login_required(login_url='/connexion')
def user_view(request):

    users = []
    cards_user = []
    all_users = User.objects.all().values()

    for user in all_users:
        if user.get('username') != request.user.username and user.get('username') != 'admin':
            users.append(user)

    if request.GET.get('user'): # get user collection
        user = User.objects.get(username=request.GET.get('user'))
        cards_user = user.card_set.all()


    return render(request, 'files/users.html', {
        'users':users,
        'cards_user': cards_user
    })


@login_required(login_url='/connexion')
def shop_view(request):

    # Preparing database #

    module_dir = os.path.dirname(__file__) # load cards.json
    file_path = os.path.join(module_dir, 'cards.json')
    with open(file_path) as f:
        data = json.load(f)

    if not Card.objects.all(): # populate database with cards from json
        for card in data['Classic']:
            if ('name' in card and 'health' in card and 'attack' in card
            and 'text' in card and 'cost' in card and 'img' in card):
                Card.objects.create(
                    name=card.get('name'),
                    cost=card.get('cost'),
                    health=card.get('health'),
                    attack=card.get('attack'),
                    text=card.get('text'),
                    img=card.get('img'))

    if not Deck.objects.filter(official=True): # create two official decks
        cards = Card.objects.all()
        for x in range(0, 2):
            name_deck = random_name_deck()
            new_deck = Deck.objects.create(
                name=name_deck,
                official=True)
            random_card_tmp = []
            deck_cost = 0
            for y in range(0, 30):
                random_card = random.choice(cards)
                while random_card in random_card_tmp: # check unicity random
                    random_card = random.choice(cards)
                Deck_Card(deck_key=new_deck,card_key=random_card).save() # create deck_card relation
                deck_cost += random_card.cost
                random_card_tmp.append(random_card)
            Deck.objects.filter(id=new_deck.id).update(cost=deck_cost)

    # Shopping #

    cards = Card.objects.all()
    decks = Deck.objects.filter(official=True)
    next_cards = activate_paginator(request, cards, 8)

    if request.method == 'POST': # buy card
        card_selected = cards.get(id=int(request.POST.get('id')))
        occurrence = (User_Card.objects.filter(user_key=request.user.id)
                            .filter(card_key=card_selected).count())
        if occurrence < 2 :
            User_Card(user_key=request.user,card_key=card_selected).save()
            user_profile = Profile.objects.get(user=request.user)
            user_profile.treasure -= card_selected.cost
            user_profile.save()

    # if(request.GET.get('deck_btn')): # buy deck
    #     element,num = request.GET['deck_btn'].split('_')
    #     if DeckOrigin.objects.filter(id=int(num)):
    #         list_new_idcard = []
    #         deck_origin = DeckOrigin.objects.filter(id=int(num))
    #         for id_card in deck_origin.values()[0].get('cards'):
    #             card_origin = CardOrigin.objects.filter(id=int(id_card))
    #             card_user = Card.objects.create( # create card_user from card_origin
    #                 name=card_origin.values()[0].get('name'),
    #                 cost=card_origin.values()[0].get('cost'),
    #                 health=card_origin.values()[0].get('health'),
    #                 attack=card_origin.values()[0].get('attack'),
    #                 text=card_origin.values()[0].get('text'),
    #                 user=request.user
    #             )
    #             list_new_idcard.append(card_user.id)
    #         deck_user = Deck.objects.create( # create deck_user from deck_origin with new id_card
    #             name=deck_origin.values()[0].get('name'),
    #             cards=list_new_idcard,
    #             cost=deck_origin.values()[0].get('cost'),
    #             user=request.user
    #         )
    #         minus_treasury(request, deck_origin.values()[0].get('cost'))
    #     return HttpResponseRedirect('/boutique')

    return render(request, 'files/shop.html', {
        'cards': next_cards,
        'decks': decks
    })


@login_required(login_url='/connexion')
def collection_view(request):

    cards_user = request.user.card_set.all()
    next_cards = activate_paginator(request, cards_user, 8)

    if request.method == 'POST': # sell card
        card_selected = cards_user.filter(id=int(request.POST.get('id')))[0]
        cards_found = User_Card.objects.filter(user_key=request.user, card_key=card_selected)
        cards_found[0].delete() # may have 2 same cards so delete 1° one
        user_profile = Profile.objects.get(user=request.user)
        user_profile.treasure += card_selected.cost
        user_profile.save()

    # if(request.GET.get('deck_btn')): # sell deck
    #     element,num = request.GET['deck_btn'].split('_')
    #     if Deck.objects.filter(id=int(num)):
    #         deck_user = Deck.objects.filter(id=int(num))
    #         for idcard in deck_user.values()[0].get('cards'): # remove card inside decks_user
    #             Card.objects.filter(id=int(idcard)).delete()
    #         plus_treasury(request, deck_user.values()[0].get('cost'))
    #         deck_user.delete()
    #     return HttpResponseRedirect('/collection')


    return render(request, 'files/collection.html',{
        'cards_user': next_cards
        # 'decks_user': decks_user
    })


@login_required(login_url='/connexion')
def create_deck_view(request):

    cards_user = request.user.card_set.all()
    next_cards = activate_paginator(request, cards_user, 8)
    decks = Deck.objects.all()

    if request.POST.get('name_deck'): # save deck
        if request.user.deck_set.all().count() == 4: # check if 4 user_decks exists
            data = { 'failed': 'fail_4_decks' }
            return JsonResponse(data)
        else:
            img = ''
            name_deck = request.POST.get('name_deck')
            if name_deck != '' and decks.filter(name=name_deck).exists() != True:
                new_deck = Deck(
                    name= name_deck,
                    img= img,
                )
                new_deck.save()
                new_deck.user.add(request.user)
                data = { 'failed': 'success' }
                return JsonResponse(data)
            else:
                data = { 'failed': 'fail_deck_exists' }
                return JsonResponse(data)

    if request.POST.get('card_to_deck'):
        new_deck = Deck.objects.get(name=request.POST.get('deck_created'))

        if Deck_Card.objects.filter(deck_key=new_deck).count() == 30:
            data = { 'failed': 'fail_30_cards' }
            return JsonResponse(data)
        else:
            card = Card.objects.get(id=int(request.POST.get('card_to_deck')))
            if (Deck_Card.objects.filter(deck_key=new_deck, card_key=card).exists()
                and User_Card.objects.filter(card_key=card,user_key=request.user).count() == 1):
                data = { 'failed': 'alone_card' }
                return JsonResponse(data)
            if Deck_Card.objects.filter(deck_key=new_deck, card_key=card).count() == 2:
                data = { 'failed': 'twice_card' }
                return JsonResponse(data)
            else:
                Deck_Card(deck_key=new_deck,card_key=card).save()
                data = { 'failed': 'success' }
                return JsonResponse(data)


    return render(request, 'files/create-deck.html',{
        'cards_user': next_cards
    })


@login_required(login_url='/connexion')
def exchange_view(request):

    all_users = User.objects.all().values()
    cards_user = request.user.card_set.all()
    cards_assignee = []
    users = []

    for user in all_users:
        if user.get('username') != request.user.username and user.get('username') != 'admin':
            users.append(user)

    if request.GET.get('user'): # get user collection
        user = User.objects.get(username=request.GET.get('user'))
        cards_assignee = user.card_set.all()

    if(request.GET.get('exchange_btn')): # sell card
        previous_url = request.META.get('HTTP_REFERER')
        try:
            previous_url.split('?')[1]
        except:
            return HttpResponseRedirect('/echanger')
        else:
            if 'user' in previous_url.split('?')[1]:
                assignee_name = previous_url.split('=')[1]
                assignee = User.objects.get(username=assignee_name)
                all_cards_assignee = assignee.card_set.all()
                creator = request.user
                cards_creator = request.GET.getlist('cards_creator_selected')
                print('\nHERE IS CARD CREATOR => ',cards_creator,'\n')
                cards_assignee = request.GET.getlist('cards_assignee_selected')
                print('\nHERE IS CARD ASSIGNEE => ',cards_assignee,'\n')
                if len(cards_assignee) > 0 or len(cards_creator) > 0:
                    new_exchange = Exchange.objects.create(
                        creator=creator,
                        assignee=assignee
                    )
                    for id_card in list(map(int, cards_creator)):
                        print('\nHERE IS CARD CREATOR => ',Card.objects.get(id=id_card),'\n')
                        Exchange_Card(
                            exchange_key=new_exchange,
                            card_key=Card.objects.get(id=id_card)
                        ).save()
                    for id_card in list(map(int, cards_assignee)):
                        print('\nHERE IS CARD ASSIGNEE => ',Card.objects.get(id=id_card),'\n')
                        Exchange_Card(
                            exchange_key=new_exchange,
                            card_key=Card.objects.get(id=id_card),
                            creator_assignee = 1
                        ).save()
                return HttpResponseRedirect('/echanger')


    return render(request, 'files/exchange.html',{
        'users':users,
        'cards_user':cards_user,
        'cards_assignee':cards_assignee
    })


@login_required(login_url='/connexion')
def forum_view(request):

    all_posts = Post.objects.all().values()
    posts = []

    for post in all_posts:
        current_post = {
            'title': post['title'],
            'date': post['date'],
            'user': User.objects.get(id=post['user_id']),
            'content': post['content'],
        }
        posts.append(current_post)

    if request.method == 'POST': # post
        form = PostForm(data=request.POST)
        if form.is_valid():
            Post.objects.create(
                title=request.POST.get("title"),
                date= datetime.date.today(),
                user=request.user,
                content=request.POST.get("content")
            )

            return HttpResponseRedirect('/forum')

    else:
        form = PostForm()


    return render(request, 'files/forum.html', {
        'posts': posts,
        'form': form
    })

    # return render(request, 'files/forum.html')


@login_required(login_url='/connexion')
def preparation_view(request):

    # users = []
    # all_users = User.objects.all().values()
    # decks_user = Deck.objects.filter(user__username=request.user.username)

    # for user in all_users:
    #     if user.get('username') != request.user.username and user.get('username') != 'admin':
    #         users.append(user)

    # if(request.GET.get('jcj_btn')): # jcj
    #     data = request.GET
    #     print('\nHERE IS DATA => ',data,'\n')

    # if(request.GET.get('ia_btn')): # ia
    #     data = request.GET
    #     Fight.objects.create(user=request.user, deck_user=data.get('deck_selected'))
    #     redirection = str('/combat/?type=ia&deck=' + data.get('deck_selected'))

    #     return HttpResponseRedirect(redirection)


    # return render(request, 'files/preparation.html', {
    #     'users':users,
    #     'decks_user': decks_user
    # })

    return render(request, 'files/preparation.html')


@login_required(login_url='/connexion')
def fight_view(request):

    # data = request.GET
    # deck_user = Deck.objects.get(id=data.get('deck'))
    # all_origin_cards = CardOrigin.objects.all().values()
    # cards_user = []
    # cards_ia = []

    # for id_card in deck_user.cards:
    #     card_user_fight = Card.objects.get(id=id_card)
    #     cards_user.append(card_user_fight)

    # if data.get('type') == 'ia':
    #     # print('\nFIGHT IA\n')
    #     for i in range(30):
    #         # print('\ni => ',i,'\n')
    #         random_card = random.choice(all_origin_cards)
    #         cards_ia.append(random_card)
    #     # print('\nRANDOM CARD => ',random_card,'\n')
    # else:
    #     print('\nFIGHT OPPONENT\n')


    # return render(request, 'files/fight.html',{
    #     'type': data.get('type'),
    #     'cards_user':cards_user,
    #     'deck_user':deck_user,
    #     'cards_ia':cards_ia
    # })

    return render(request, 'files/fight.html')

