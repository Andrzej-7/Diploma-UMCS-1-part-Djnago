# exchange/views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import redirect, render
from .forms import OrderForm
from .models import Order
from django.http import HttpResponse


wallets = {
    'ETH': 'ETH3bf69a829c08f1ee28b0c013c937209a',
    'XMR': 'XMR1ddb778e2b24b6e065a112080869c5f3',
    # Додайте інші варіанти криптовалют
}

def home(request):
    return render(request, 'exchange/home.html')

def custom_login(request):
    return render(request, 'registration/login.html')

def custom_register(request):
    return render(request, 'registration/register.html')

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)  # Збереження нового замовлення
            crypto_from = form.cleaned_data['crypto_from']
            order.site_wallet = wallets.get(crypto_from, 'адреса за замовчуванням')
            order.save()  # Збереження замовлення з встановленим site_wallet
            return redirect('confirm_order', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'exchange/create_exchange_order.html', {'form': form})



def confirm_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        order.is_paid = True  # Встановіть, що замовлення оплачено

        crypto_from = order.crypto_from  # Отримайте вибір криптовалюти
        order.site_wallet = wallets.get(crypto_from, 'адреса за замовчуванням')
        order.save()  # Збережіть зміни

       

    return render(request, 'exchange/confirm_order.html', {'order': order})


from django.shortcuts import render



def thank_you(request):
    
    return render(request, 'exchange/thank_you.html')



def mark_order_as_processed(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.is_processed = True
    order.save()
    return JsonResponse({'message': f'Замовлення {order_id} було оброблено.'})


def check_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return JsonResponse({'is_processed': order.is_processed})


def mark_order_as_paid(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.is_paid = True
    order.save()
    return JsonResponse({'message': 'Оплата підтверджена.'})

def check_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return JsonResponse({'is_processed': order.is_processed})
