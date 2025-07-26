from django import forms
from listings.models import ProductListing

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductListing
        fields = ['title', 'description', 'price', 'sku', 'quantity', 'cuisine', 'is_active']
        