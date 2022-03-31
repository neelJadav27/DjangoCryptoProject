from django.urls import path
from . import views

app_name = 'crypto'
urlpatterns = [
    path('', views.index, name='index'),
    path("login/", views.login, name='login'),
    path("signup/", views.signup, name='signup'),
    path("home/", views.home, name='home'),
    path("profile/", views.profile, name='profile'),
    path('<str:cryptoName>', views.cryptoName, name='cryptoName'),
]
