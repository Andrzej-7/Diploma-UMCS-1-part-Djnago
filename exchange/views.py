# views.py

from django.contrib import messages
import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .models import Order
from .forms import UserRegisterForm, OrderForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .forms import loginForm

api = '39a10038-46ef-40df-840f-87a402232775'

wallets = {

    'ETH': 'ETH3bf69a829c08f1ee28b0c013c937209a', 'XMR': 'XMR1ddb778e2b24b6e065a112080869c5f3',
    'BTC': 'BTCmbHfnpaZjKFvyi1okTjJJusN455paPH', 'DAI': 'DAIA385E6A13f935665B3b44897Dd12E4018f5903C',
    'BNB': 'BNB82917412Ab41D614509a44652933204d4aea7Cb', 'USDT': 'USDTfJyNxCws7gsjDRdJmVqovy4zuQsR9w',
    'LTC': 'LTCtpGGzSCfR7V6WRmL168BNwGvDi2joRm', 'XLM': 'XLMfQIK63R2NETJM7T673EAMZN4RJLLGP3',
    'ADA': 'ADA2N1FfmbHfnpaZmVqovyEAMZNpaZjK', 'XRP': 'XRP13f93NETJM7T6Ab41D614509a446VqovyEAM'

}



def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.User = request.user

            crypto_from = form.cleaned_data['crypto_from']
            order.site_wallet = wallets.get(crypto_from, 'No wallet provided')
            order.you_get = convert_crypto(form.cleaned_data['amount'], form.cleaned_data['crypto_from'],
                                           form.cleaned_data['crypto_to'], api)

            order.save()
            return redirect('confirm_order', uuid=order.uuid)
    else:
        form = OrderForm()

    return render(request, 'exchange/create_exchange_order.html', {'form': form})


def confirm_order(request, uuid):
    order = get_object_or_404(Order, uuid=uuid)

    if request.method == 'POST':
        order.is_paid = True
        crypto_from = order.crypto_from
        order.site_wallet = wallets.get(crypto_from, 'example adress')
        order.save()

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
        return redirect('confirm_order', uuid=order.uuid)
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


def get_conversion_rate(from_currency, to_currency, api):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    headers = {
        'X-CMC_PRO_API_KEY': api,
        'Accepts': 'application/json'
    }


    parameters = {
        'symbol': ','.join([from_currency, to_currency]),
        'convert': 'USD'
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    if 'data' in data and from_currency in data['data'] and to_currency in data['data']:
        from_price = data['data'][from_currency]['quote']['USD']['price']
        to_price = data['data'][to_currency]['quote']['USD']['price']
        rate = from_price / to_price
        return rate
    else:
        raise ValueError("API response is missing 'data' or currency information.")


def convert_crypto(amount, from_currency, to_currency, api):
    rate = get_conversion_rate(from_currency, to_currency, api)
    converted_amount = float(amount) * float(rate)
    return converted_amount


def convert_currency(request):
    try:
        amount = float(request.GET.get('amount', 0))
    except ValueError:
        return JsonResponse({'error': 'Invalid amount value'}, status=400)

    from_currency = request.GET.get('from_currency', 'BTC')
    to_currency = request.GET.get('to_currency', 'BTC')

    converted_amount = convert_crypto(amount, from_currency, to_currency, api)
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
                messages.error(request, "Invalid username or password.", extra_tags='login')

        else:
            messages.error(request, "Form data is not valid.", extra_tags='login')

    else:
        form = loginForm()

    return render(request, 'registration/login.html', {'form': form})


def aml_policy(request):
    return render(request, 'agreements/aml.html')


def user_agreement(request):
    return render(request, 'agreements/aml.html')
