from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Order
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


class OrderAdmin(admin.ModelAdmin):
    list_display = ['email', 'crypto_from']

    actions = ['mark_as_processed']

    def mark_as_processed(self, request, queryset):
        count = queryset.update(is_processed=True)
        self.message_user(request, f"{count} замовлення(-ь) було(-о) оброблено.")
    
    mark_as_processed.short_description = "Обробити замовлення"


admin.site.register(Order, OrderAdmin)
