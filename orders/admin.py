from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'price', 'quantity', 'subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'city', 'total', 'created_at']
    list_filter = ['city', 'created_at']
    search_fields = ['full_name', 'email', 'phone']
    readonly_fields = ['total', 'created_at']
    inlines = [OrderItemInline]
