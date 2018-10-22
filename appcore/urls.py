from django.urls import path
from . import views
from django.contrib.auth.views import login

urlpatterns = [
    path('', views.welcome_view, name="welcome"),
    path('inscription/', views.register_view, name="register"),
    path('connexion/', views.login_view, name="login"),
    # path('deconnexion/', views.logout_view, name="logout"),
    path('accueil/', views.home_view, name="home"),
]
