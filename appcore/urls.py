from django.urls import path
from . import views
# from django.contrib.auth.views import login
from django.contrib.auth import views as auth_views


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
    path('fight/', views.fight_view, name="fight"),

    # path('mot-de-passe/', views.PasswordResetView, name="password_reset"),
    # path('mot-de-passe/done/', views.PasswordResetDoneView, name="password_reset_done"),
    path('mot-de-passe/', auth_views.PasswordResetView.as_view(
        template_name='files/password_reset.html'
    ), name="password_reset"),
    path('mot-de-passe/fait/', auth_views.PasswordResetDoneView.as_view(
        template_name='files/password_reset_done.html'
    ), name="password_reset_done"),
    path('mot-de-passe-confirmation/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='files/password_reset_confirm.html'
    ), name="password_reset_confirm"),
]
