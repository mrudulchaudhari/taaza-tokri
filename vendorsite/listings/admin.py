# vendorsite/listings/admin.py

from django.contrib import admin
from .models import ProductListing

@admin.register(ProductListing)
class ProductListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'supplier', 'price', 'quantity', 'is_active', 'sku')
    list_filter = ('is_active', 'supplier', 'cuisine')
    search_fields = ('title', 'sku', 'supplier__name')
    list_editable = ('price', 'quantity', 'is_active')