import django.contrib.auth
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from datetime import date
from .models import *
from .models import Crypto as Cr
from .forms import *
import numpy as np
import pandas as pd

import yfinance as yf
from yahooquery import Screener
import plotly.graph_objs as go
from datetime import datetime, timedelta
import yfinance as yf
import plotly.graph_objs as go
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
                    django.contrib.auth.login(req, user)

            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    django.contrib.auth.login(req, user)
                    return redirect("crypto:index")
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
            data = User.objects.create_user(email=email, username=email, dob=dob, first_name=firstName,
                                            last_name=lastName, password=password, sex=sex, phoneNo=phoneNo)
            data.save()
            return HttpResponse("Registered")
        else:
            return HttpResponse("Invalid data")
    else:
        signUpForm = SignUpForm()

    return render(req, "signup.html", {"signUpForm": signUpForm})


def home(req):
    countData = Cr.objects.filter().count()
    cryptoData = Cr.objects.filter(id__gte=1, id__lte=10).values()
    data = pd.DataFrame()
    for a in cryptoData:
        df1 = yf.download(a['alias'] + "-USD", start=getPrevDate(7)[0], end=getPrevDate(7)[1], interval="90m")
        df1["currency"] = a['alias']
        data = data.append(df1)

    data = data.reset_index(level=0)
    data = data.drop('Adj Close', axis=1)

    return render(req, "home.html", {'columns': data.columns, 'rows': data.to_dict('records'), "cryptoData": cryptoData,
                                     "range": range(1, int(countData / 10) + 1)})


def cryptoName(req, cryptoName):

    data = pd.DataFrame()
    if req.method == "POST":

        if req.POST.get("oneDay"):
            df1 = yf.download(cryptoName + "-USD", start=getPrevDate(1)[0], end=getPrevDate(1)[1], interval="5m")
        elif req.POST.get("sevenDays"):
            print("second")
            df1 = yf.download(cryptoName + "-USD", start=getPrevDate(7)[0], end=getPrevDate(7)[1], interval="15m")
        elif req.POST.get("fifteenDays"):
            print("second")
            df1 = yf.download(cryptoName + "-USD", start=getPrevDate(15)[0], end=getPrevDate(15)[1], interval="15m")
        elif req.POST.get("oneMonth"):
            df1 = yf.download(cryptoName + "-USD", start=getPrevDate(30)[0], end=getPrevDate(30)[1], interval="30m")
        elif req.POST.get("twoMonths"):
            df1 = yf.download(cryptoName + "-USD", start=getPrevDate(59)[0], end=getPrevDate(59)[1], interval="90m")
            print("third")

    else:
        df1 = yf.download(cryptoName + "-USD", start=getPrevDate(1)[0], end=getPrevDate(1)[1], interval="5m")

    df1["currency"] = cryptoName

    data = data.append(df1)

    data = data.reset_index(level=0)
    data = data.drop('Adj Close', axis=1)
    cryptoData = Cr.objects.filter(alias=cryptoName).values()
    print(cryptoData)
    return render(req, "cryptodetail.html", {'column': data.columns, 'rows': data.to_dict('records'), 'cryptoName': cryptoName,'cryptoDetails':cryptoData})


def defineCrypto(req, currency_name):
    data = yf.download(currency_name + "-USD", start=getPrevDate()[0], end=getPrevDate()[1], interval="90m")
    return render(req, 'defineCrypto.html', {'columns': data.columns, 'rows': data.to_dict('records')})


def profile(req):
    userInfo = req.user
    return render(req, 'profile.html', {'user_info': userInfo})


def getPrevDate():
    today = datetime.today() + timedelta(1)
    yesterday = datetime.today() - timedelta(2)
    today = today.strftime('%Y-%m-%d')
    yesterday = yesterday.strftime('%Y-%m-%d')
    return yesterday, today


def getPrevDate(prevDate):
    today = datetime.today()
    if prevDate == 15:
        previousDate = datetime.today() - timedelta(15)
    elif prevDate == 30:
        previousDate = datetime.today() - timedelta(30)
    elif prevDate == 59:
        previousDate = datetime.today() - timedelta(59)
    elif prevDate == 7:
        previousDate = datetime.today() - timedelta(7)
    elif prevDate == 1:
        previousDate = datetime.today() - timedelta(1)
    today = today.strftime('%Y-%m-%d')
    previousDate = previousDate.strftime('%Y-%m-%d')
    return previousDate, today

