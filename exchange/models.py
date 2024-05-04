# models.py

from django.db import models
from django.contrib.auth.models import User
import uuid

ETH = "ETH"
XMR = "XMR"
DAI = "DAI"
DASH = "DASH"
Dogecoin = "Dogecoin"
Bitcoin = "BTC"
USDT = "USDT"
BNB = "BNB"
LTC = "LTC"
XLM = "XLM"
ADA = "ADA"
XRP = "XRP"

cryptoChoises = ((ETH, "eth"),
                 (XMR, "xmr"),
                 (DAI, "dai"),
                 (DASH, "dash"),
                 (Dogecoin, "dogecoin"),
                 (Bitcoin, "bitcoin"),

                 (LTC, "LTC"),
                 (XLM, "stellar"),
                 (ADA, "cardano"),
                 (BNB, "BNB"),
                 (XRP, "XRP"),
                 (USDT, "usdt"))


class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField()
    crypto_from = models.CharField(max_length=255, choices=cryptoChoises)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    recipient_wallet = models.CharField(max_length=255)
    crypto_to = models.CharField(max_length=255, choices=cryptoChoises)
    is_paid = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)
    site_wallet = models.CharField(max_length=255, blank=True, null=True)
    you_get = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)


class CryptoCurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f'Order {self.id}'
