from django.urls import path
from . import views

app_name = 'crypto'
urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login, name='login'),
    path("logout", views.logout, name='logout'),
    path("signup", views.signup, name='signup'),
    path("home", views.home, name='home'),
    path("profile", views.profile, name='profile'),
    path("makepayment", views.makePayment, name='makepayment'),
    path("add_payment", views.paymentDetails, name='add_payment'),
    path("editProfile", views.editProfile, name='editProfile'),
    path('<str:cryptoName>', views.cryptoName, name='cryptoName'),
]
