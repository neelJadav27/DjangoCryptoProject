from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime


class Demo(models.Model):
    name = models.CharField(max_length=20)


class User(User):
    reg = RegexValidator(regex="^[0-9]{10}$", message="THIS WILL ONLY ALLOW TEN DIGIT NUMBERS")
    phoneNo = models.PositiveIntegerField(validators=[reg], blank=False, null=False)
    sexChoices = [('M', "Male"), ('F', "Female"), ('O', "Others")]
    sex = models.CharField(max_length=1, choices=sexChoices, default='F')
    dob = models.DateField(null=False, blank=False)


class Crypto(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    alias = models.CharField(max_length=30, null=False, blank=False)
    available = models.FloatField(default=1000)
    description = models.CharField(max_length=2000, blank=True)
    url = models.TextField(default="https://raw.githubusercontent.com/neelJadav27/DjangoCryptoProject/main/NoImage.png")


class Wallet(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    cryptoRate = models.FloatField(null=False, blank=False)
    buyRate = models.FloatField(null=False, blank=False)
    quantity = models.FloatField(null=False, blank=False)
    operationChoice = [('B', "Buy"), ('S', "Sell")]
    type = models.CharField(max_length=1, choices=operationChoice, default='B')
    paymentDate = models.DateField(default=datetime.now())


class PaymentInfo(models.Model):
    reg = RegexValidator(regex="^[0-9]{12}$", message="THIS WILL ONLY ALLOW TWELVE DIGIT NUMBERS")
    cvvReg = RegexValidator(regex="^[0-9]{3}$", message="THIS WILL ONLY ALLOW THREE DIGIT NUMBERS")
    cardHolderName = models.CharField(max_length=100,blank=False,null=False)
    cardNo = models.BigIntegerField(validators=[reg], blank=False, null=False)
    expiryDate = models.DateField(null=False, blank=False)
    CVV = models.PositiveIntegerField(validators=[cvvReg], blank=False, null=False)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

