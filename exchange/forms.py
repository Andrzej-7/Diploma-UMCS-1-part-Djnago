# exchange/forms.py

from django import forms
from .models import Order

    

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'crypto_from', 'amount', 'recipient_wallet', 'crypto_to','site_wallet']

        widgets = {
            'site_wallet': forms.HiddenInput() #приховування йобаного поля 'site_wallet' щоб вона не вилазаила на головній сторінці
        }


    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['site_wallet'].widget = forms.HiddenInput()