from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['paid_by', 'paid_to', 'amount', 'method', 'status', 'paid_at']
    list_filter = ['status', 'method']