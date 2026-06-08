from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_editable = ['is_active']
    list_display_links = ['username']
    fieldsets = [
        ('Login Info', {'fields': ['username', 'password']}),
        ('Personal Info', {'fields': ['first_name', 'last_name', 'email']}),
        ('Permissions', {'fields': ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']}),
        ('Important Dates', {'fields': ['last_login', 'date_joined']}),
    ]
