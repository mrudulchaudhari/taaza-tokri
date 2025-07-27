# vendorsite/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# This is the correct configuration for your Custom User model.
# It uses the default fields that exist on your model.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'groups']

admin.site.register(CustomUser, CustomUserAdmin)