from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

from .forms import *


def index(req):
    return HttpResponse("Welcome!")


def login(req):
    if req.method == "POST":
        logInForm = LogInForm(req.POST)
        if logInForm.is_valid():
            email = logInForm.cleaned_data['email']
            return HttpResponse(email)
        else:
            return HttpResponse("Invalid data")
    else:
        logInForm = LogInForm()

    return render(req, "login.html", {"logInForm": logInForm})


def signup(req):
    if req.method == "POST":
        signUpForm = SignUpForm(req.POST)
        if signUpForm.is_valid():

            return HttpResponse("Nice")
        else:
            return HttpResponse("Invalid data")
    else:
        signUpForm = SignUpForm()

    return render(req, "signup.html", {"signUpForm": signUpForm})
