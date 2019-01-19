from django.urls import path
from . import views
from django.contrib.auth.views import login

urlpatterns = [
    path('', views.welcome_view, name="welcome"),
    path('inscription/', views.register_view, name="register"),
    path('connexion/', views.login_view, name="login"),
    path('tableau-de-bord/', views.home_view, name="home"),
    path('compte/', views.account_view, name="account"),
    path('boutique/', views.shop_view, name="shop"),
    path('collection/', views.collection_view, name="collection"),
    path('collection/deck/', views.collection_deck_view, name="collection_deck"),
    path('deck/cartes/<int:id>/', views.collection_deck_cards_view, name="collection_deck_cards"),
    path('utilisateurs/', views.user_view, name="utilisateurs"),
    path('creation-de-deck/', views.create_deck_view, name="create-deck"),
    path('echanger/', views.exchange_view, name="exchange"),
    path('forum/', views.forum_view, name="forum"),
    path('preparation/', views.preparation_view, name="preparation"),
    path('combat/', views.fight_view, name="fight"),
]
