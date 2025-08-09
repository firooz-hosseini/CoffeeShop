from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ['id', 'mobile', 'email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['mobile']
    ordering = ['-id']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    readonly_fields = ['last_login', 'date_joined']