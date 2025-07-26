from django.contrib import admin
# CHANGED: Import your actual model
from .models import ProductListing

# This makes the admin interface more user-friendly
@admin.register(ProductListing)
class ProductListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'vendor', 'price', 'quantity', 'is_active')
    list_filter = ('is_active', 'vendor', 'cuisine')
    search_fields = ('title', 'sku', 'vendor__name')