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
]
