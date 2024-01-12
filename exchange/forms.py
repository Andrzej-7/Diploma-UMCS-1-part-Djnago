#forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'crypto_from', 'amount', 'recipient_wallet', 'crypto_to', 'site_wallet']

        widgets = {
            'site_wallet': forms.HiddenInput(),  # Приховування поля 'site_wallet'
            
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))
    

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

        


