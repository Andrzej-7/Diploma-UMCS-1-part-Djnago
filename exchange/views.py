#views.py
from django.contrib import messages
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import redirect, render
from .forms import OrderForm
from .models import Order
from django.http import HttpResponse
from .forms import UserRegisterForm, OrderForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .forms import loginForm
from django.contrib.auth.models import User





wallets = {
    'ETH': 'ETH3bf69a829c08f1ee28b0c013c937209a',
    'XMR': 'XMR1ddb778e2b24b6e065a112080869c5f3',
    #інші варіанти криптовалют
}

def home(request):
    return render(request, 'exchange/home.html')


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            # Прив'язка користувача до замовлення
            if request.user.is_authenticated:
                order.user = request.user

            crypto_from = form.cleaned_data['crypto_from']
            order.site_wallet = wallets.get(crypto_from, 'common adress')

            # Отримайте і збережіть обчислену суму з прихованого поля
            order.you_get = request.POST.get('converted_amount', 0)

            order.save()
            return redirect('confirm_order', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'exchange/create_exchange_order.html', {'form': form})




def confirm_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        order.is_paid = True  # Встановіть, що замовлення оплачено

        crypto_from = order.crypto_from  # Отримайте вибір криптовалюти
        order.site_wallet = wallets.get(crypto_from, 'example adress')
        order.save()  # Збережіть зміни

       

    return render(request, 'exchange/confirm_order.html', {'order': order})






def mark_order_as_processed(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.is_processed = True
    order.save()
    return JsonResponse({'message': f'Order {order_id} is processed.'})


def check_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return JsonResponse({'is_processed': order.is_processed})


def mark_order_as_paid(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.is_paid = True
    order.save()
    return JsonResponse({'message': 'Payment confirmed. We have 15 min to process this order'})

def check_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return JsonResponse({'is_processed': order.is_processed})




def get_conversion_rate(from_currency, to_currency, api_key):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        'X-CMC_PRO_API_KEY': api_key,
        'Accepts': 'application/json'
    }
    parameters = {
        'symbol': ','.join([from_currency, to_currency]),
        'convert': 'USD'  # Використовуємо USD як проміжну валюту для конвертації
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    from_price = data['data'][from_currency]['quote']['USD']['price']
    to_price = data['data'][to_currency]['quote']['USD']['price']

    rate = from_price / to_price
    return rate

def convert_crypto(amount, from_currency, to_currency, api_key):
    rate = get_conversion_rate(from_currency, to_currency, api_key)
    converted_amount = amount * rate
    return converted_amount



def convert_currency(request):
    if request.method == "GET":
        amount = float(request.GET.get('amount', 0))
        from_currency = request.GET.get('from_currency', 'BTC')
        to_currency = request.GET.get('to_currency', 'USDT')
        api_key = '39a10038-46ef-40df-840f-87a402232775'  #API ключ

        converted_amount = convert_crypto(amount, from_currency, to_currency, api_key)
        return JsonResponse({'converted_amount': converted_amount})

    return JsonResponse({'error': 'Invalid request'}, status=400)



def custom_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('create_exchange_order')
        else:
            #зберігаємо помилки форми
            form_errors = form.errors
            messages.error(request, form_errors, extra_tags='registration')
            #очищуємо поля форми
            form = UserRegisterForm()
            #додаємо збережені помилки до нової форми
            form._errors = form_errors
            #код зверху потрібний для того щоб після очищення форми помилки зберігались
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})






def custom_login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)  
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('create_exchange_order')
            else:
                # Використовуємо тег 'login' для помилок входу
                messages.error(request, "Invalid username or password.", extra_tags='login')
                
        else:
            messages.error(request, "Form data is not valid.", extra_tags='login')
            
    else:
        form = loginForm()

    return render(request, 'registration/login.html', {'form': form})

