from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'slug', 'product_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview', 'product_count', 'created_at']
    fieldsets = [
        ('Basic Info', {'fields': ['name', 'slug']}),
        ('Media', {'fields': ['image', 'image_preview']}),
        ('Description', {'fields': ['description']}),
        ('Info', {'fields': ['product_count', 'created_at']}),
    ]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:4px;" />', obj.image.url)
        return mark_safe('<span style="color:#999;">No image</span>')
    image_preview.short_description = 'Image'

    def product_count(self, obj):
        count = obj.products.count()
        return format_html('<b>{}</b> product{}', count, 's' if count != 1 else '')
    product_count.short_description = 'Products'
