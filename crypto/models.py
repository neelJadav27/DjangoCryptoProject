from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime
from django.utils.timezone import now


class Demo(models.Model):
    name = models.CharField(max_length=20)


class User(User):
    reg = RegexValidator(regex="^[0-9]{10}$", message="THIS WILL ONLY ALLOW TEN DIGIT NUMBERS")
    phoneNo = models.PositiveIntegerField(validators=[reg], blank=False, null=False)
    sexChoices = [('M', "Male"), ('F', "Female"), ('O', "Others")]
    sex = models.CharField(max_length=1, choices=sexChoices, default='F')
    dob = models.DateField(null=False, blank=False)
    walletBalance = models.DecimalField(max_digits=100, decimal_places=4, default=0)

    def __str__(self):
        return str(self.id)


class Crypto(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    alias = models.CharField(max_length=30, null=False, blank=False)
    available = models.FloatField(default=1000)
    description = models.CharField(max_length=2000, blank=True)
    url = models.TextField(default="https://raw.githubusercontent.com/neelJadav27/DjangoCryptoProject/main/NoImage.png")

    def __str__(self):
        return str(self.id)


class Wallet(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    # What was the price when user bough crypto
    cryptoRate = models.FloatField(null=False, blank=False)
    # How much worth user bought or sold the crypto at
    amount = models.FloatField(null=False, blank=False)
    # How many crypto user bought
    quantity = models.FloatField(null=False, blank=False)
    operationChoice = [('B', "Buy"), ('S', "Sell")]
    type = models.CharField(max_length=1, choices=operationChoice, default='B')
    paymentDate = models.DateField(default=now)

    def _str_(self):
        return str(self.id)


class PaymentInfo(models.Model):
    reg = RegexValidator(regex="^[0-9]{12}$", message="THIS WILL ONLY ALLOW TWELVE DIGIT NUMBERS")
    cvvReg = RegexValidator(regex="^[0-9]{3}$", message="THIS WILL ONLY ALLOW THREE DIGIT NUMBERS")
    cardHolderName = models.CharField(max_length=100, blank=False, null=False)
    cardNo = models.BigIntegerField(validators=[reg], blank=False, null=False)
    expiryDate = models.DateField(null=False, blank=False)
    CVV = models.PositiveIntegerField(validators=[cvvReg], blank=False, null=False)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
