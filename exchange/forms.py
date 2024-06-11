#forms

import django
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    agreement = forms.BooleanField(required=True, error_messages={'required': "Confirm user agreement."})

    class Meta:
        model = Order
        fields = ['email', 'crypto_from', 'amount', 'recipient_wallet', 'crypto_to', 'site_wallet']
        widgets = {
            'site_wallet': forms.HiddenInput(),  #hide 'site_wallet'
        }

    def clean_recipient_wallet(self):
        wallet = self.cleaned_data.get('recipient_wallet')
        crypto_to = self.cleaned_data.get('crypto_to')

        if not crypto_to:
            crypto_to = self.data.get('crypto_to')


        if not wallet:
            raise ValidationError("Wallet address is required.")
        if not crypto_to:
            raise ValidationError("Crypto to field is required.")

        if not wallet.startswith(crypto_to) or len(wallet) < 10 or not wallet.isalnum():
            raise ValidationError("Wallet address is incorrect")

        return wallet



    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None or amount <= 0:
            raise ValidationError("The amount must be greater than zero.")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        crypto_from = cleaned_data.get('crypto_from')
        crypto_to = cleaned_data.get('crypto_to')


        if crypto_from == crypto_to:
            self.add_error('crypto_to', "Select different cryptocurrencies.")

        return cleaned_data


class UserRegisterForm(UserCreationForm):
    username = django.forms.CharField(widget=django.forms.TextInput(attrs={'placeholder': 'Username'}))
    email = django.forms.EmailField(widget=django.forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    password1 = django.forms.CharField(widget=django.forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = django.forms.CharField(widget=django.forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class loginForm(django.forms.Form):
    username = django.forms.CharField(widget=django.forms.TextInput(attrs={'placeholder': 'Username'}))
    password = django.forms.CharField(widget=django.forms.PasswordInput(attrs={'placeholder': 'Password'}))
