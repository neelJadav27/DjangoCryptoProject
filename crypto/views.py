import django.contrib.auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import *
from .models import Crypto as Cr
from .forms import *
import pandas as pd
import yfinance as yf
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
        return HttpResponse("You are not logged in. Please Login")


def logout(req):
    if req.user.is_authenticated:
        django.contrib.auth.logout(req)
        # user is logged in
        return redirect('crypto:login')
    else:
        # user is not logged in
        return redirect('crypto:login')


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
                    req.session.set_expiry(7200)
                    return redirect("crypto:profile")
                else:
                    status = "User account disabled"
            else:
                status = "Username or password is wrong"
        else:
            status = "Invalid Data"
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
            try:
                userData = User.objects.create_user(email=email, username=email, dob=dob, first_name=firstName,
                                                    last_name=lastName, password=password, sex=sex, phoneNo=phoneNo)
                userData.save()

                logInForm = LogInForm()
                status = ""
                context = {
                    "logInForm": logInForm,
                    "status": "",
                    "status2": "Signup successful",
                }

                return render(req, "login.html", context)
            except:
                return render(req, "signup.html", {"signUpForm": signUpForm, "status": "User already exists"})

        else:
            return render(req, "signup.html", {"signUpForm": signUpForm, "status": "Invalid Data"})
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
        ticker_yahoo = yf.Ticker(a['alias'] + "-USD")
        ticket_history = ticker_yahoo.history(period='1d', interval='1d')
        ticket_info = ticker_yahoo.info
        try:
            currentPrice = (ticket_history.tail(1)['Close'].iloc[0])
        except:
            currentPrice = 0
        circulatingSupply = ticket_info["circulatingSupply"]
        marketCap = ticket_info["marketCap"]
        volume = ticket_info['volume24Hr']

        updateData = {'currentPrice': currentPrice, 'circulatingSupply': circulatingSupply, 'marketCap': marketCap,
                      'volume': volume}
        a.update(updateData)
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
        "range": range(int(pageRange[0]), int(pageRange[1]))
    }

    return render(req, "home.html", context)


def cryptoName(req, cryptoName):
    data = pd.DataFrame()

    ticker_yahoo = yf.Ticker(cryptoName + "-USD")
    ticket_history = ticker_yahoo.history(period='1d', interval='1d')
    ticket_info = ticker_yahoo.info
    try:
        currentPrice = (ticket_history.tail(1)['Close'].iloc[0])
    except:
        currentPrice = 0
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


# def defineCrypto(req, currency_name):
#     data = yf.download(currency_name + "-USD", start=getPrevDate(7)[0], end=getPrevDate(7)[1], interval="90m")
#     return render(req, 'defineCrypto.html', {'columns': data.columns, 'rows': data.to_dict('records')})


def editProfile(req):
    if not req.user.is_authenticated:
        return redirect('crypto:login')

    if req.method == "POST":
        editProfileForm = EditProfileDetails(req.POST)
        if editProfileForm.is_valid():

            User.objects.filter(username=req.user.username).update(
                first_name=editProfileForm.cleaned_data['first_name'],
                last_name=editProfileForm.cleaned_data['last_name'],
                phoneNo=editProfileForm.cleaned_data['phoneNo'])
            # editProfileForm.save()
            return render(req, "profile.html", {"status2": "Information updated"})
        else:
            # for key in req.POST.keys():
            #     if field.erros
            # status = ""
            # for field in editProfileForm:
            #     for error in field.errors:
            #         status += field.name + " " + error + " \n"
            #         print(field)
            #         print(field.name)
            #         print(error)

            print(editProfileForm.errors)
            userData = User.objects.filter(username=req.user.username).values().first()
            context = {
                "userData": userData,
                "formError": editProfileForm
            }
            return render(req, "editProfile.html", context)

    else:
        userData = User.objects.filter(username=req.user.username).values().first()
        context = {
            "userData": userData,
        }
        return render(req, "editProfile.html", context)


def profile(req):
    if not req.user.is_authenticated:
        return redirect('crypto:login')

    userData = User.objects.filter(username=req.user.username).values().first()
    paymentInfo = PaymentInfo.objects.filter(userId=userData['id']).values().first()

    history = Wallet.objects.filter(userId=userData['id']).values()

    for data in history:
        cryptoData = Cr.objects.filter(id=data['crypto_id']).values().first()
        data.update({'cryptoData': cryptoData})
    if paymentInfo is not None:
        updateCardInfo = {'cardNo': '**** **** ****' + str(paymentInfo['cardNo'])[12:16], 'CVV': '***'}
        paymentInfo.update(updateCardInfo)
    context = {
        "userData": userData,
        "paymentInfo": paymentInfo,
        "history": history
    }
    return render(req, 'profile.html', context)


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


# add credit card details
def paymentDetails(req):
    if not req.user.is_authenticated:
        return redirect('crypto:login')

    if req.method == "POST":
        paymentForm = PaymentDetailsForm(req.POST)

        if req.POST.get("EditCard"):
            userData = User.objects.get(username=req.user.username)
            cardInfo = PaymentInfo.objects.filter(userId=userData).values().first()
            initial = {
                'cardHolderName': cardInfo['cardHolderName'],
                'cardNo': cardInfo['cardNo'],
                'CVV': cardInfo['CVV'],
                'expiryDate': cardInfo['expiryDate'],
            }

            paymentForm = PaymentDetailsForm(initial=initial)

            return render(req, 'addpayment.html', {'paymentForm': paymentForm})

        elif paymentForm.is_valid():
            userData = User.objects.get(username=req.user.username)
            cardInfo = PaymentInfo.objects.filter(userId=userData).values().first()

            if cardInfo is None:
                paymentData = paymentForm.save(commit=False)
                paymentData.userId = User.objects.get(username=req.user.username)
                paymentForm.save()
                redirectToWhere = req.GET.get("cryptoName", "")

                if redirectToWhere != "":
                    return render(req, 'redirect.html', {'cryptoName': redirectToWhere})
            else:
                cardHolderName = paymentForm.cleaned_data['cardHolderName']
                cardNo = paymentForm.cleaned_data['cardNo']
                expiryDate = paymentForm.cleaned_data['expiryDate']
                CVV = paymentForm.cleaned_data['CVV']
                PaymentInfo.objects.filter(userId=userData).update(cardHolderName=cardHolderName, cardNo=cardNo,
                                                                   expiryDate=expiryDate, CVV=CVV)
                # return redirect('crypto:profile')
            #print("good")
            return render(req, "profile.html", {"status2": "Information updated"})

        else:
            # error list here
            return redirect('crypto:add_payment')
    else:
        paymentForm = PaymentDetailsForm()

    context = {
        "paymentForm": paymentForm,
    }
    return render(req, "addpayment.html", context)


def makePayment(req):
    if not req.user.is_authenticated:
        return redirect('crypto:login')

    if req.method == "POST":
        if req.POST.get("Buy"):
            cryptoValue = req.POST.get("cryptoValue")

            cryptoName = req.GET.get('cryptoName')
            cryptoDbData = Cr.objects.filter(alias=cryptoName).values().first()
            userData = User.objects.filter(username=req.user.username).values().first()

            if cryptoDbData['available'] - float(cryptoValue) >= 0:
                Cr.objects.filter(alias=cryptoName).update(available=cryptoDbData['available'] - float(cryptoValue))
            else:
                return render(req, 'redirect.html', {'cryptoName': cryptoName})

            userId = User.objects.get(username=req.user.username)
            cryptoId = Cr.objects.get(alias=cryptoName)

            ticker_yahoo = yf.Ticker(cryptoName + "-USD")
            ticket_history = ticker_yahoo.history(period='1d', interval='1d')
            try:
                currentPrice = (ticket_history.tail(1)['Close'].iloc[0])
            except:
                currentPrice = 0

            amount = float(currentPrice) * float(cryptoValue)

            if amount >= userData['walletBalance']:
                # below amount will be taken from user's card after using user's wallet balance
                cardBalance = amount - float(userData['walletBalance'])
                # RESET BALANCE TO 0
                User.objects.filter(username=req.user.username).update(walletBalance=0)
            else:
                # below amount will REMAIN after using user's wallet balance
                remainingWalletBalance = float(userData['walletBalance']) - float(amount)
                # UPDATE THE BALANCE WITH BALANCE-AMOUNT
                User.objects.filter(username=req.user.username).update(
                    walletBalance=remainingWalletBalance)

            walletData = Wallet(userId=userId, crypto=cryptoId, cryptoRate=currentPrice,
                                amount=amount, quantity=cryptoValue, type='B')
            walletData.save()

            return render(req, "profile.html", {"status2": "Buy completed"})
            #return redirect('crypto:profile')

        elif req.POST.get("Sell"):

            cryptoName = req.GET.get("cryptoName", "")

            if cryptoName == "":
                return render(req, 'redirect.html', {'cryptoName': cryptoName})

            cryptoValue = float(req.POST.get("sellCryptoValue"))

            userData = User.objects.filter(username=req.user.username).values().first()
            cryptoData = Cr.objects.filter(alias=cryptoName).values()
            walletInfo = Wallet.objects.filter(userId=userData['id'], crypto=cryptoData.first()['id']).values()

            ticker_yahoo = yf.Ticker(cryptoName + "-USD")
            ticket_history = ticker_yahoo.history(period='1d', interval='1d')
            try:
                currentPrice = (ticket_history.tail(1)['Close'].iloc[0])
            except:
                currentPrice = 0

            cryptoAmount = 0

            for data in walletInfo:
                if data['type'] == 'B':
                    cryptoAmount += data['quantity']
                elif data['type'] == 'S':
                    cryptoAmount -= data['quantity']

            usdAmount = float(currentPrice) * float(cryptoValue)

            if cryptoValue > cryptoAmount:
                return render(req, 'redirect.html', {'cryptoName': cryptoName})

            userId = User.objects.get(username=req.user.username)
            cryptoId = Cr.objects.get(alias=cryptoName)

            walletData = Wallet(userId=userId, crypto=cryptoId, cryptoRate=currentPrice,
                                amount=usdAmount, quantity=cryptoValue, type='S')
            walletData.save()
            walletBalance = float(userData['walletBalance']) + usdAmount
            User.objects.filter(username=req.user.username).update(walletBalance=walletBalance)
            return render(req, "profile.html", {"status2": "Sell completed"})
            #return redirect('crypto:profile')

        elif req.POST.get("MakeTransaction"):

            cryptoName = req.GET.get("cryptoName", "")

            if cryptoName == "":
                return HttpResponse("Crypto Name Missing. Unable to make payment")

            userData = User.objects.filter(username=req.user.username).values()
            paymentData = PaymentInfo.objects.filter(userId=userData.first()['id']).values()
            cryptoData = Cr.objects.filter(alias=cryptoName).values()
            walletInfo = Wallet.objects.filter(userId=userData.first()['id'], crypto=cryptoData.first()['id']).values()

            cardInfo = paymentData.first()

            if paymentData.count() > 0:
                isPaymentAdded = True
                updateCardInfo = {'cardNo': '**** **** ****' + str(cardInfo['cardNo'])[12:16], 'CVV': '***'}
                cardInfo.update(updateCardInfo)
            else:
                isPaymentAdded = False

            cryptoAmount = 0
            userHasBought = False
            if walletInfo.count() > 0:
                cryptoAmount = 0
                for data in walletInfo:
                    if data['type'] == 'B':
                        cryptoAmount += data['quantity']
                    elif data['type'] == 'S':
                        cryptoAmount -= data['quantity']

                if cryptoAmount < 0:
                    return HttpResponse("Crypto Value below 0")
                elif cryptoAmount > 0:
                    userHasBought = True

            ticker_yahoo = yf.Ticker(cryptoName + "-USD")
            ticket_history = ticker_yahoo.history(period='1d', interval='1d')
            ticket_info = ticker_yahoo.info
            try:
                currentPrice = (ticket_history.tail(1)['Close'].iloc[0])
            except:
                currentPrice = 0
            circulatingSupply = ticket_info["circulatingSupply"]
            marketCap = ticket_info["marketCap"]
            context = {
                "isPaymentAdded": isPaymentAdded,
                "userHasBought": userHasBought,
                "cryptoData": cryptoData.first(),
                "userData": userData.first(),
                "currentPrice": currentPrice,
                "cardInfo": cardInfo,
                "circulatingSupply": circulatingSupply,
                "marketCap": marketCap,
                # 'usdAmount': usdAmount,
                'cryptoAmount': cryptoAmount,
            }

            return render(req, "makepayment.html", context)
        else:
            return HttpResponse("Unknown Operation")
    else:

        cryptoName = req.GET.get("cryptoName", "")

        if cryptoName == "":
            return HttpResponse("Crypto Name Missing. Unable to make payment")

        userData = User.objects.filter(username=req.user.username).values()
        paymentData = PaymentInfo.objects.filter(userId=userData.first()['id']).values()
        cryptoData = Cr.objects.filter(alias=cryptoName).values()
        walletInfo = Wallet.objects.filter(userId=userData.first()['id'], crypto=cryptoData.first()['id']).values()

        cardInfo = paymentData.first()

        if paymentData.count() > 0:
            isPaymentAdded = True
            updateCardInfo = {'cardNo': '**** **** ****' + str(cardInfo['cardNo'])[12:16], 'CVV': '***'}
            cardInfo.update(updateCardInfo)
        else:
            isPaymentAdded = False

        cryptoAmount = 0
        userHasBought = False
        if walletInfo.count() > 0:
            cryptoAmount = 0
            for data in walletInfo:
                if data['type'] == 'B':
                    cryptoAmount += data['quantity']
                elif data['type'] == 'S':
                    cryptoAmount -= data['quantity']

            if cryptoAmount < 0:
                return HttpResponse("Crypto Value below 0")
            elif cryptoAmount > 0:
                userHasBought = True

        ticker_yahoo = yf.Ticker(cryptoName + "-USD")
        ticket_history = ticker_yahoo.history(period='1d', interval='1d')
        ticket_info = ticker_yahoo.info
        try:
            currentPrice = (ticket_history.tail(1)['Close'].iloc[0])
        except:
            currentPrice = 0
        circulatingSupply = ticket_info["circulatingSupply"]
        marketCap = ticket_info["marketCap"]
        context = {
            "isPaymentAdded": isPaymentAdded,
            "userHasBought": userHasBought,
            "cryptoData": cryptoData.first(),
            "userData": userData.first(),
            "currentPrice": currentPrice,
            "cardInfo": cardInfo,
            "circulatingSupply": circulatingSupply,
            "marketCap": marketCap,
            # 'usdAmount': usdAmount,
            'cryptoAmount': cryptoAmount,
        }

    return render(req, "makepayment.html", context)
