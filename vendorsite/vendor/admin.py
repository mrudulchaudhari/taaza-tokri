# vendorsite/vendor/admin.py

from django.contrib import admin
from .models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'user', 'phone_number', 'city')
    search_fields = ('shop_name', 'city', 'user__username')