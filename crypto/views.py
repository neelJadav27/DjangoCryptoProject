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
        # print(req.user)
        # data = User.objects.filter(username=req.user.username).values()
        # print(data)
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

    context = {
        "logInForm": logInForm,
        "status": status
    }

    return render(req, "login.html", context)


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

    context = {
        "signUpForm": signUpForm
    }

    return render(req, "signup.html", context)


def home(req):
    countData = Cr.objects.filter().count()

    if req.method == "POST":
        for key in req.POST.keys():
            if key.startswith('page'):
                action = int(key[4:])
                page = action
                start = action * 10 - 10
                end = action * 10
                cryptoData = Cr.objects.filter().order_by("id").values()[start:end]
                break
    else:
        cryptoData = Cr.objects.filter().order_by("id").values()[:10]
        page = 1

    data = pd.DataFrame()
    for a in cryptoData:
        df1 = yf.download(a['alias'] + "-USD", start=getPrevDate(1)[0], end=getPrevDate(1)[1], interval="90m")
        df1["currency"] = a['alias']
        data = data.append(df1)

    data = data.reset_index(level=0)
    data = data.drop('Adj Close', axis=1)

    pageRange = getPageRange(page, 5, (countData / 10))

    context = {
        "page": page,
        'columns': data.columns,
        'rows': data.to_dict('records'),
        "cryptoData": cryptoData,
        "range": range(pageRange[0], pageRange[1])
    }

    return render(req, "home.html", context)


def cryptoName(req, cryptoName):
    data = pd.DataFrame()

    ticker_yahoo = yf.Ticker(cryptoName + "-USD")
    ticket_history = ticker_yahoo.history()
    ticket_info = ticker_yahoo.info
    currentPrice = (ticket_history.tail(1)['Close'].iloc[0])
    circulatingSupply = ticket_info["circulatingSupply"]
    marketCap = ticket_info["marketCap"]

    if req.method == "POST":
        if req.POST.get("oneDay"):
            df1 = yf.download(cryptoName + "-USD", start=getPrevDate(1)[0], end=getPrevDate(1)[1], interval="5m")
        elif req.POST.get("sevenDays"):
            df1 = yf.download(cryptoName + "-USD", start=getPrevDate(7)[0], end=getPrevDate(7)[1], interval="15m")
        elif req.POST.get("fifteenDays"):
            df1 = yf.download(cryptoName + "-USD", start=getPrevDate(15)[0], end=getPrevDate(15)[1], interval="15m")
        elif req.POST.get("oneMonth"):
            df1 = yf.download(cryptoName + "-USD", start=getPrevDate(30)[0], end=getPrevDate(30)[1], interval="30m")
        elif req.POST.get("twoMonths"):
            df1 = yf.download(cryptoName + "-USD", start=getPrevDate(59)[0], end=getPrevDate(59)[1], interval="90m")

    else:
        df1 = yf.download(cryptoName + "-USD", start=getPrevDate(1)[0], end=getPrevDate(1)[1], interval="5m")

    df1["currency"] = cryptoName

    data = data.append(df1)

    data = data.reset_index(level=0)
    data = data.drop('Adj Close', axis=1)
    cryptoData = Cr.objects.filter(alias=cryptoName).values()

    context = {
        "marketCap": marketCap,
        "circulatingSupply": circulatingSupply,
        "currentPrice": currentPrice,
        'column': data.columns,
        'rows': data.to_dict('records'),
        'cryptoName': cryptoName,
        'cryptoDetails': cryptoData,
    }

    return render(req, "cryptodetail.html", context)


def defineCrypto(req, currency_name):
    data = yf.download(currency_name + "-USD", start=getPrevDate(7)[0], end=getPrevDate(7)[1], interval="90m")
    return render(req, 'defineCrypto.html', {'columns': data.columns, 'rows': data.to_dict('records')})


def editProfile(req):
    if req.method == "POST":
        editProfileForm = EditProfileDetails(req.POST)
        if editProfileForm.is_valid():
            userId = req.user.username
            User.objects.filter(username=req.user.username).update(first_name=editProfileForm.cleaned_data['first_name'],last_name=editProfileForm.cleaned_data['last_name'],email=editProfileForm.cleaned_data['email'],phoneNo=editProfileForm.cleaned_data['phoneNo'])
            # editProfileForm.save()
            return redirect('crypto:profile')
    else:
        userData = User.objects.filter(username=req.user.username).values().first()
        print(userData)
        context = {
            "userData": userData,
        }
        return render(req, "editProfile.html",context)

def profile(req):
    userData = User.objects.filter(username=req.user.username).values().first()
    paymentInfo = PaymentInfo.objects.filter(userId=userData['id']).values().first()
    print(paymentInfo)
    print(userData)
    context = {
        "userData":userData,
        "paymentInfo":paymentInfo
    }
    return render(req, 'profile.html', context)



# def getPrevDate():
#     today = datetime.today() + timedelta(1)
#     yesterday = datetime.today() - timedelta(2)
#     today = today.strftime('%Y-%m-%d')
#     yesterday = yesterday.strftime('%Y-%m-%d')
#     return yesterday, today


def getPrevDate(prevDate):
    today = datetime.today()
    previousDate = datetime.today() - timedelta(prevDate)
    today = today.strftime('%Y-%m-%d')
    previousDate = previousDate.strftime('%Y-%m-%d')
    return previousDate, today


def getPageRange(pageNumber, onEachSide, totalPage):
    range1 = max(pageNumber - onEachSide + 1, 1)
    range2 = min(pageNumber + onEachSide + 1, totalPage)

    return range1, range2


def paymentDetails(req):
    if req.method == "POST":
        paymentForm = PaymentDetailsForm(req.POST)
        if paymentForm.is_valid():
            paymentData = paymentForm.save(commit=False)
            paymentData.userId = User.objects.get(username=req.user.username)
            paymentForm.save()
            redirectToWhere = req.GET.get("cryptoName", "")

            if redirectToWhere != "":
                return render(req, 'redirect.html',{'cryptoName':redirectToWhere})

            return HttpResponse("success")
        else:
            return HttpResponse("Invalid data")
    else:
        paymentForm = PaymentDetailsForm()

    context = {
        "paymentForm": paymentForm,
    }
    return render(req, "carddetails.html", context)


def makePayment(req):
    if req.method == "POST":
        if req.POST.get("Buy"):

            return HttpResponse("Buy Button")
            # if success full then save data and print the message

        elif req.POST.get("Sell"):
            return HttpResponse("Sell Button")
            # if sucessfull then save data
        elif req.POST.get("MakeTransaction"):
            cryptoName = req.GET.get("cryptoName", "")

            if cryptoName == "":
                return HttpResponse("Crypto Name Missing. Unable to make payment")

            userData = User.objects.filter(username=req.user.username).values()
            userData2 = User.objects.get(username=req.user.username)
            paymentData = PaymentInfo.objects.filter(userId=userData2).values()
            cryptoData = Cr.objects.filter(alias=cryptoName).values()
            cryptoData2 = Cr.objects.get(alias=cryptoName)
            walletInfo = Wallet.objects.filter(userId=userData2, crypto=cryptoData2)

            if paymentData.count() > 0:
                isPaymentAdded = True
            else:
                isPaymentAdded = False

            if walletInfo.count() > 0:
                userHasBought = True
            else:
                userHasBought = False

            ticker_yahoo = yf.Ticker(cryptoName + "-USD")
            ticket_history = ticker_yahoo.history()
            ticket_info = ticker_yahoo.info
            currentPrice = (ticket_history.tail(1)['Close'].iloc[0])
            circulatingSupply = ticket_info["circulatingSupply"]
            marketCap = ticket_info["marketCap"]

            context = {
                "isPaymentAdded": isPaymentAdded,
                "cryptoData": cryptoData,
                "userData": userData,
                "currentPrice": currentPrice,
                "circulatingSupply": circulatingSupply,
                "marketCap": marketCap,
                "userHasBought": userHasBought,
                "cryptoName": cryptoName,
            }
            #  print(userHasBought)
            #   context["userHasBought"]=userHasBought

            return render(req, "makepayment.html", context)
        else:
            return HttpResponse("Unknown Operation")
    else:

        cryptoName = req.GET.get("cryptoName", "")

        if cryptoName == "":
            return HttpResponse("Crypto Name Missing. Unable to make payment")

        userData = User.objects.filter(username=req.user.username).values()
        userData2 = User.objects.get(username=req.user.username)
        paymentData = PaymentInfo.objects.filter(userId=userData2).values()
        cryptoData = Cr.objects.filter(alias=cryptoName).values()
        cryptoData2 = Cr.objects.get(alias=cryptoName)
        walletInfo = Wallet.objects.filter(userId=userData2, crypto=cryptoData2)

        if paymentData.count() > 0:
            isPaymentAdded = True
        else:
            isPaymentAdded = False

        if walletInfo.count() > 0:
            userHasBought = True
        else:
            userHasBought = False

        ticker_yahoo = yf.Ticker(cryptoName + "-USD")
        ticket_history = ticker_yahoo.history()
        ticket_info = ticker_yahoo.info
        currentPrice = (ticket_history.tail(1)['Close'].iloc[0])
        circulatingSupply = ticket_info["circulatingSupply"]
        marketCap = ticket_info["marketCap"]

        context = {
            "isPaymentAdded": isPaymentAdded,
            "cryptoData": cryptoData,
            "userData": userData,
            "currentPrice": currentPrice,
            "circulatingSupply": circulatingSupply,
            "marketCap": marketCap,
            "userHasBought": userHasBought,
            "cryptoName": cryptoName,
        }
    #  print(userHasBought)
    #   context["userHasBought"]=userHasBought

    return render(req, "makepayment.html", context)

