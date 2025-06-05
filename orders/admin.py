from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'order_type', 'quantity', 'created_at', 'due_date')
    list_filter = ('order_type', 'created_at')
    search_fields = ('user__username', 'book__title')
