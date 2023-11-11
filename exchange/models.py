from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

ETH = "ETH"
XMR = "XMR"
DAI = "DAI"
DASH = "DASH"
Dogecoin = "Dogecoin"


cryptoChoises = ((ETH, "eth"),
                (XMR, "xmr"),
                (DAI, "dai"),
                (DASH, "dash"),
                (Dogecoin, "dogecoin"),)


class Order(models.Model):
    email = models.EmailField()
    crypto_from = models.CharField(max_length=255, choices=cryptoChoises)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    recipient_wallet = models.CharField(max_length=255)
    crypto_to = models.CharField(max_length=255, choices=cryptoChoises)
    is_paid = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False) 
    site_wallet = models.CharField(max_length=255, blank=True, null=True)



class CryptoCurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)



    def __str__(self):
        return f'Order {self.id}'
    

