from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class Demo(models.Model):
    name = models.CharField(max_length=20)


class User(User):
    reg=RegexValidator(regex="^[0-9]{10}$",message="THIS WILL ONLY ALLOW TEN DIGIT NUMBERS")
    phoneNo = models.PositiveIntegerField(validators=[reg])
    sexChoices=[('M',"Male"),('F',"Female"),('O',"Others")]
    sex=models.CharField(max_length=1,choices=sexChoices,default='F')


class Crypto(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=30)
    available = models.PositiveIntegerField(default=1000)
    description = models.CharField(max_length=200)


class Wallet(models.Model):
    userId = models.ForeignKey(User , on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto , on_delete=models.CASCADE)
    currRate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    cumulativeAmount = models.PositiveIntegerField()
    sold = models.PositiveIntegerField()

