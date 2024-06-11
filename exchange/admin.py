#admin

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Order
from django.utils.html import format_html
from django.shortcuts import get_object_or_404


class OrderAdmin(admin.ModelAdmin):
    list_display = ['email', 'crypto_from', 'crypto_to', 'is_paid', 'recipient_wallet', 'process_order_link', 'is_processed']

    def process_order_link(self, obj):
        return format_html('<a class="button" href="{}">Process Order</a>',
                           reverse('admin:order_process', args=[obj.pk]))

    process_order_link.short_description = 'Process Order'

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/process/', self.admin_site.admin_view(self.process_order), name='order_process'),
        ]
        return custom_urls + urls

    def process_order(self, request, object_id):
        order = get_object_or_404(Order, pk=object_id)
        order.is_processed = True
        order.save()
        self.message_user(request, "Order has been processed.")
        return HttpResponseRedirect("../")


admin.site.register(Order, OrderAdmin)
