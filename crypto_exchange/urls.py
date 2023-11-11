# exchange/urls.py

from django.urls import path
from exchange import views
from django.contrib import admin
from exchange.views import mark_order_as_processed, confirm_order

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', views.create_order, name='create_exchange_order'),
    path('login/', views.custom_login, name='login'),
    path('register/', views.custom_register, name='register'),
    path('create_order/', views.create_order, name='create_order'),
    path('confirm_order/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('mark_as_processed/<int:order_id>/', mark_order_as_processed, name='mark_as_processed'),
    path('mark_as_paid/<int:order_id>/', views.mark_order_as_paid, name='mark_as_paid'),
    path('check_order_status/<int:order_id>/', views.check_order_status, name='check_order_status'),

    
]
