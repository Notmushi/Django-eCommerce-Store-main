from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Product


class StockFilter(admin.SimpleListFilter):
    title = 'stock status'
    parameter_name = 'stock_status'

    def lookups(self, request, model_admin):
        return [
            ('in', 'In Stock'),
            ('out', 'Out of Stock'),
            ('low', 'Low Stock (< 10)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'in':
            return queryset.filter(stock__gt=0)
        if self.value() == 'out':
            return queryset.filter(stock=0)
        if self.value() == 'low':
            return queryset.filter(stock__gt=0, stock__lt=10)
        return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'category', 'price', 'stock', 'featured', 'available', 'created_at']
    list_filter = ['featured', 'available', 'category', StockFilter, 'created_at']
    search_fields = ['name', 'description', 'category__name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['featured', 'available', 'stock', 'price']
    list_display_links = ['name']
    readonly_fields = ['image_preview', 'created_at']
    fieldsets = [
        ('Basic Info', {'fields': ['name', 'slug', 'category', 'price', 'stock']}),
        ('Media', {'fields': ['image', 'image_preview']}),
        ('Description', {'fields': ['description']}),
        ('Status', {'fields': ['featured', 'available']}),
        ('Timestamps', {'fields': ['created_at']}),
    ]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:4px;" />', obj.image.url)
        return mark_safe('<span style="color:#999;">No image</span>')
    image_preview.short_description = 'Image'
