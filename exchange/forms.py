#forms.py

import django
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order



class OrderForm(django.forms.ModelForm):


    class Meta:
        model = Order
        fields = ['email', 'crypto_from', 'amount', 'recipient_wallet', 'crypto_to', 'site_wallet']

        widgets = {
            'site_wallet': django.forms.HiddenInput(),  #Приховування поля 'site_wallet'
        }


    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)




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
