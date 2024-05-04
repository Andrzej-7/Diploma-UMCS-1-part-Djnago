# views.py
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
import uuid

wallets = {
    'ETH': 'ETH3bf69a829c08f1ee28b0c013c937209a',
    'XMR': 'XMR1ddb778e2b24b6e065a112080869c5f3',
    # інші варіанти криптовалют
}


def home(request):
    return render(request, 'exchange/home.html')


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            return redirect('confirm_order', uuid=order.uuid)
    else:
        form = OrderForm()

    return render(request, 'exchange/create_exchange_order.html', {'form': form})


def confirm_order(request, uuid):
    order = get_object_or_404(Order, uuid=uuid)

    if request.method == 'POST':
        order.is_paid = True  # Встановіть, що замовлення оплачено

        crypto_from = order.crypto_from  # Отримайте вибір криптовалюти
        order.site_wallet = wallets.get(crypto_from, 'example adress')
        order.save()  # Збережіть зміни

    return render(request, 'exchange/confirm_order.html', {'order': order})


def mark_order_as_processed(request, uuid):
    order = get_object_or_404(Order, uuid=uuid)
    order.is_processed = True
    order.save()
    return JsonResponse({'message': f'Order {order.uuid} is processed.'})





def mark_order_as_paid(request, uuid):
    if request.method == 'POST':
        order = get_object_or_404(Order, uuid=uuid)
        order.is_paid = True
        order.save()
        request.session['order_status'] = 'Payment confirmed. We have 15 min to process this order'
        return redirect('confirm_order', uuid=order.uuid)  # Redirect to the confirmation page
    return JsonResponse({'message': 'Invalid request method'}, status=405)





def check_order_status(request, uuid):
    order = get_object_or_404(Order, uuid=uuid)
    status_message = request.session.get('order_status', '')
    return JsonResponse({
        'is_processed': order.is_processed,
        'is_paid': order.is_paid,
        'status_message': status_message
    }, status=200)


def cancel_order(request, uuid):
    order = get_object_or_404(Order, uuid=uuid)
    order.delete()
    return redirect('create_exchange_order')


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
    try:
        amount = float(request.GET.get('amount', 0))
    except ValueError:
        return JsonResponse({'error': 'Invalid amount value'}, status=400)

    from_currency = request.GET.get('from_currency', 'BTC')
    to_currency = request.GET.get('to_currency', 'BTC')
    api_key = '39a10038-46ef-40df-840f-87a402232775'  # API ключ

    converted_amount = convert_crypto(amount, from_currency, to_currency, api_key)
    return JsonResponse({'converted_amount': converted_amount})


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
            # зберігаємо помилки форми
            form_errors = form.errors
            messages.error(request, form_errors, extra_tags='registration')
            # очищуємо поля форми
            form = UserRegisterForm()
            # додаємо збережені помилки до нової форми
            form._errors = form_errors
            # код зверху потрібний для того щоб після очищення форми помилки зберігались
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
