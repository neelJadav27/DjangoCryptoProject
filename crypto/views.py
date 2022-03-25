import django.contrib.auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# Create your views here.
from datetime import date
from .models import *
from .models import Crypto as Cr
from .forms import *
import numpy as np
import pandas as pd
#Data Source
import yfinance as yf
#Data viz
import plotly.graph_objs as go
#date
from datetime import datetime, timedelta



def index(req):
    if not req.user:
        return HttpResponse("User does not exist")
    elif req.user.is_authenticated:
        return HttpResponse("Logged in")
    else:
        return HttpResponse("Please login")


def login(req):
    if req.method == "POST":
        logInForm = LogInForm(req.POST)
        if logInForm.is_valid():
            email = logInForm.cleaned_data['email']
            password = logInForm.cleaned_data["password"]
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    django.contrib.auth.login(req,user)
                    return redirect("index")
                else:
                    status = "User account disabled"
            else:
                status = "Username and/or password is wrong"
        else:
            return HttpResponse("Invalid data")
    else:
        logInForm = LogInForm()
        status = ""
    return render(req, "login.html", {"logInForm": logInForm, "status": status})


def signup(req):

    if req.method == "POST":
        signUpForm = SignUpForm(req.POST)
        if signUpForm.is_valid():
            email = signUpForm.cleaned_data['email']
            signUpForm = signUpForm.save(commit=False)
            signUpForm.username = email
            signUpForm.save()

            return HttpResponse("Registered")
        else:
            return HttpResponse("Invalid data")
    else:
        signUpForm = SignUpForm()

    return render(req, "signup.html", {"signUpForm": signUpForm})



def home(req):

    Currencies= Cr.objects.filter(available__gte=1).values('alias')
    data = pd.DataFrame()
    for a in Currencies:
        #print(a['alias'])
        df1= yf.download(a['alias']+"-USD", start=GetPrevDate()[0], end=GetPrevDate()[1], interval="1m")
        df1["currency"]=a['alias']
        data =data.append(df1)

    print(data)
    return HttpResponse("ASDASDAS")



def GetPrevDate():
  Today=datetime.today() + timedelta(1)
  Yesterday=datetime.today()- timedelta(2)
  Today=Today.strftime('%Y-%m-%d')
  Yesterday=Yesterday.strftime('%Y-%m-%d')
  return Yesterday,Today
