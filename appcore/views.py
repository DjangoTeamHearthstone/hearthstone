from django.contrib import messages
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import RegisterForm, LoginForm, ModifyForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Card, Deck, Profile, Exchange, Post, Fight
from django.template.defaulttags import register
from django.conf.urls.static import static
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import datetime, requests, random, os, json


# Global functions #
def plus_treasury(request, cost):
    treasury = Profile.objects.filter(user__username=request.user.username).values()[0].get('treasure')
    treasury += cost
    return Profile.objects.filter(user__username=request.user.username).update(treasure=treasury)

def minus_treasury(request, cost):
    treasury = Profile.objects.filter(user__username=request.user.username).values()[0].get('treasure')
    treasury -= cost
    return Profile.objects.filter(user__username=request.user.username).update(treasure=treasury)

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

def preparing_listid_cardselected(request, cards_selected):
    list_idcard_selected = []
    [list_idcard_selected.append(int(x)) for x in cards_selected]
    return list_idcard_selected

def preparing_list_exchange(request, list_base):
    list_data = []
    [list_data.append(Card.objects.get(id=x)) for x in list_base]
    return list_data

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
    list_creators = []
    list_l_cards_creator = []
    list_l_cards_assignee = []
    exchange_received_id = []

    exchanges_received = Exchange.objects.filter(assignee__username=request.user.username)
    [ exchange_received_id.append(exchanges_received.values()[c].get('id'))
        for c, x in enumerate(exchanges_received)]
    for exchange in exchanges_received:
        list_creators.append(User.objects.get(id=exchange.creator_id))
        list_l_cards_creator.append(preparing_list_exchange(request, exchange.cards_creator))
        list_l_cards_assignee.append(preparing_list_exchange(request, exchange.cards_assignee))
    zipped = list(zip(list_creators, list_l_cards_creator, list_l_cards_assignee, exchange_received_id))

    if(request.GET.get('accept_btn')): # accept exchange
        data = request.GET
        exchange_accepted = Exchange.objects.get(id=data.get('accept_btn'))
        [Card.objects.filter(id=card).update(user=exchange_accepted.assignee)
            for card in exchange_accepted.cards_creator]
        [Card.objects.filter(id=card).update(user=exchange_accepted.creator)
            for card in exchange_accepted.cards_assignee]
        exchange_accepted.delete()
        return HttpResponseRedirect('/tableau-de-bord')

    if(request.GET.get('refuse_btn')): # refuse exchange
        data = request.GET
        exchange_refused = Exchange.objects.get(id=data.get('refuse_btn'))
        exchange_refused.delete()
        return HttpResponseRedirect('/tableau-de-bord')

    if request.method == 'POST': # logout
        logout(request)
        return HttpResponseRedirect('/')


    return render(request, 'files/home.html', {
        'exchange_received_id': exchange_received_id,
        'assignee': request.user.username,
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
        print('\nHERE IS LABELS => ', form_password.fields['password1'])
        # form_password.fields['username'].label. = "custom_css"
        # form_password.fields['password'].widget.attrs['style'] = "background:red"

        if form_password.is_valid():
            user = form_password.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.INFO, 'Hello world.')
            return redirect('account')

        else:
            messages.error(request, 'Veuillez réessayer.')

    else:
        form_password = PasswordChangeForm(request.user)
        form_password.fields['old_password'].label = 'Ancien mot de passe'
        form_password.fields['new_password1'].label = 'Nouveau mot de passe'
        form_password.fields['new_password2'].label = 'Confirmer mot de passe'
        print('\nHERE IS LABELS => ', form_password,'\n')


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

    if(request.GET.get('seebtn')): # get user collection
        userSelected = request.GET['dropdown']
        cards_user = Card.objects.filter(user__username=userSelected)


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
                while random_card in random_card_tmp:
                    random_card = random.choice(cards)
                for card_update in Card.objects.filter(id=random_card.id):
                    card_update.deck.add(new_deck.id)
                deck_cost += random_card.cost
                random_card_tmp.append(random_card)
            Deck.objects.filter(id=new_deck.id).update(cost=deck_cost)

    # Shopping #

    cards = Card.objects.all()
    decks = Deck.objects.filter(official=True)

    paginator = Paginator(cards, 8)
    page = request.GET.get('page')
    next_cards = paginator.get_page(page)

    # print('\n HERE IS CARDS => ',cards,'\n')
    # print('\n HERE IS DECKS => ',decks,'\n')

    # cards_origin = CardOrigin.objects.all()
    # decks_origin = DeckOrigin.objects.all()

    # if(request.GET.get('card_btn')): # buy card
    #     data = request.GET
    #     list_idcard_selected = preparing_listid_cardselected(request, data.getlist('cards_selected'))
    #     for idcard_selected in list_idcard_selected:
    #         if CardOrigin.objects.filter(id=idcard_selected):
    #             card_origin = CardOrigin.objects.filter(id=idcard_selected)
    #             Card.objects.create(
    #                 name=card_origin.values()[0].get('name'),
    #                 cost=card_origin.values()[0].get('cost'),
    #                 health=card_origin.values()[0].get('health'),
    #                 attack=card_origin.values()[0].get('attack'),
    #                 text=card_origin.values()[0].get('text'),
    #                 user=request.user
    #             )
    #             minus_treasury(request, card_origin.values()[0].get('cost'))

    #     return HttpResponseRedirect('/boutique')

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

    # return render(request, 'files/shop.html', {
    #     'cards_origin': cards_origin,
    #     'decks_origin': decks_origin
    # })

    return render(request, 'files/shop.html', {
        'cards': next_cards,
        'decks': decks
    })


@login_required(login_url='/connexion')
def collection_view(request):

    cards_user = Card.objects.filter(user__username=request.user.username)
    decks_user = Deck.objects.filter(user__username=request.user.username)

    list_idcard_selected = []
    if(request.GET.get('card_btn')): # sell card
        data = request.GET
        list_idcard_selected = preparing_listid_cardselected(request, data.getlist('cards_selected'))
        for idcard_selected in list_idcard_selected:
            if Card.objects.filter(id=idcard_selected):
                card_user = Card.objects.filter(id=idcard_selected)
                for deck in decks_user: # remove card from decks_user
                    new_list_deck_cards = deck.cards
                    if idcard_selected in deck.cards:
                        new_list_deck_cards.remove(idcard_selected)
                        Deck.objects.filter(id=deck.id).update(cards=new_list_deck_cards)
                        deck.cost -= card_user.values()[0].get('cost')
                        Deck.objects.filter(id=deck.id).update(cost=deck.cost)
                plus_treasury(request, card_user.values()[0].get('cost'))
                card_user.delete()
        return HttpResponseRedirect('/collection')

    if(request.GET.get('deck_btn')): # sell deck
        element,num = request.GET['deck_btn'].split('_')
        if Deck.objects.filter(id=int(num)):
            deck_user = Deck.objects.filter(id=int(num))
            for idcard in deck_user.values()[0].get('cards'): # remove card inside decks_user
                Card.objects.filter(id=int(idcard)).delete()
            plus_treasury(request, deck_user.values()[0].get('cost'))
            deck_user.delete()
        return HttpResponseRedirect('/collection')


    return render(request, 'files/collection.html',{
        'cards_user': cards_user,
        'decks_user': decks_user
    })


@login_required(login_url='/connexion')
def create_deck_view(request):

    cards_user = Card.objects.filter(user__username=request.user.username)
    decks_user = Deck.objects.filter(user__username=request.user.username)

    cost_deck = 0
    list_idcard_selected = []

    if(request.GET.get('create_deck')): # create deck
        data = request.GET
        if data.get('name_deck') == 'Nom du Deck' :
            name_deck_selected = random_name_deck(request)
        else:
            name_deck_selected = data.get('name_deck')
        list_idcard_selected = preparing_listid_cardselected(request, data.getlist('cards_selected'))
        for idcard_selected in list_idcard_selected:
            card_user = Card.objects.filter(id=idcard_selected)
            cost_deck += card_user.values()[0].get('cost')
        Deck.objects.create( # create deck_user
            name=name_deck_selected,
            cards=list_idcard_selected,
            cost=cost_deck,
            user=request.user
        )
        return HttpResponseRedirect('/creation-de-deck')


    return render(request, 'files/create-deck.html',{
        'cards_user': cards_user
    })


@login_required(login_url='/connexion')
def exchange_view(request):

    cards_creator = Card.objects.filter(user__username=request.user.username)
    users = []
    cards_assignee = []
    all_users = User.objects.all().values()

    for user in all_users:
        if user.get('username') != request.user.username and user.get('username') != 'admin':
            users.append(user)

    if(request.GET.get('seebtn')): # get user collection
        userSelected = request.GET['dropdown']
        cards_assignee = Card.objects.filter(user__username=userSelected)

    if(request.GET.get('card_btn')): # sell card
        data = request.GET
        creator = request.user
        assignee = User.objects.get(username=data.getlist('dropdown')[0])
        cards_creator = preparing_listid_cardselected(request, data.getlist('cards_creator_selected'))
        cards_assignee = preparing_listid_cardselected(request, data.getlist('cards_assignee_selected'))
        Exchange.objects.create(
            creator=creator,
            assignee=assignee,
            cards_creator=cards_creator,
            cards_assignee=cards_assignee
        )

        return HttpResponseRedirect('/echanger')


    return render(request, 'files/exchange.html',{
        'cards_creator': cards_creator,
        'cards_assignee': cards_assignee,
        'users':users
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


@login_required(login_url='/connexion')
def preparation_view(request):

    users = []
    all_users = User.objects.all().values()
    decks_user = Deck.objects.filter(user__username=request.user.username)

    for user in all_users:
        if user.get('username') != request.user.username and user.get('username') != 'admin':
            users.append(user)

    if(request.GET.get('jcj_btn')): # jcj
        data = request.GET
        print('\nHERE IS DATA => ',data,'\n')

    if(request.GET.get('ia_btn')): # ia
        data = request.GET
        Fight.objects.create(user=request.user, deck_user=data.get('deck_selected'))
        redirection = str('/combat/?type=ia&deck=' + data.get('deck_selected'))

        return HttpResponseRedirect(redirection)


    return render(request, 'files/preparation.html', {
        'users':users,
        'decks_user': decks_user
    })


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
