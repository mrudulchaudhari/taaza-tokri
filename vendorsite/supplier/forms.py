# vendorsite/supplier/forms.py

from django import forms
from listings.models import ProductListing

class ProductListingForm(forms.ModelForm):
    """
    A form for suppliers to create and update their product listings.
    """
    class Meta:
        model = ProductListing
        # These are the fields the supplier will fill out.
        fields = ['title', 'description', 'price', 'sku', 'quantity', 'cuisine']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        help_texts = {
            'sku': 'A unique code for your product, e.g., "TOMATO-RED-01".',
            'cuisine': 'The category your product best fits into.',
        }