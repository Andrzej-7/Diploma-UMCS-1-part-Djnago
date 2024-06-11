from django.db import models
from django.contrib.auth.models import User
import uuid


cryptoChoises = (

    ("ETH", "eth"), ("XMR", "xmr"), ("DAI", "dai"), ("DASH", "dash"), ("Dogecoin", "dogecoin"),
    ("BTC", "bitcoin"), ("USDT", "usdt"), ("BNB", "BNB"), ("LTC", "LTC"), ("XLM", "stellar"),
    ("ADA", "cardano"), ("XRP", "XRP")

)


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


class user(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)



    def __str__(self):
        return f'Order {self.id}'
