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
            dob = signUpForm.cleaned_data['dob']
            firstName = signUpForm.cleaned_data['first_name']
            lastName = signUpForm.cleaned_data['last_name']
            password = signUpForm.cleaned_data['password']
            sex = signUpForm.cleaned_data['sex']
            phoneNo = signUpForm.cleaned_data['phoneNo']
            data = User.objects.create_user(email=email,username=email,dob=dob,first_name=firstName,last_name=lastName,password=password,sex=sex,phoneNo=phoneNo)
            data.save()
            return HttpResponse("Registered")
        else:
            return HttpResponse("Invalid data")
    else:
        signUpForm = SignUpForm()

    return render(req, "signup.html", {"signUpForm": signUpForm})


def home(req):
    Currencies = Crypto.objects.filter(available__gte=1).values('alias')
    data = pd.DataFrame()
    for a in Currencies:
        # print(a['alias'])
        df1 = yf.download(a['alias'] + "-USD", start=GetPrevDate(2)[0], end=GetPrevDate(2)[1], interval="1m")
        df1["currency"] = a['alias']
        data = data.append(df1)

    data = data.reset_index(level=0)
    data = data.drop('Adj Close', axis=1)
    print(data)
    return render(req, 'home.html', {'columns': data.columns, 'rows': data.to_dict('records')})

def defineCrypto(req, currency_name):
    data = yf.download(currency_name + "-USD", start=GetPrevDate(90)[0], end=GetPrevDate(90)[1], interval="5m")
    return  render (req , 'defineCrypto.html',{'columns': data.columns, 'rows': data.to_dict('records')})


def profile(req):
    UserInfo= req.user
    wallet_info= Wallet.objects.filter(userId=UserInfo.id)
    return render(req, 'profile.html',{'user_info':UserInfo,'waller_info':wallet_info})

def GetPrevDate(back):
  Today=datetime.today() + timedelta(1)
  Yesterday=datetime.today()- timedelta(back)
  Today=Today.strftime('%Y-%m-%d')
  Yesterday=Yesterday.strftime('%Y-%m-%d')
  return Yesterday,Today
