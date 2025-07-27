from django import forms
from listings.models import ProductListing

class ProductListingForm(forms.ModelForm):
    class Meta:
        model = ProductListing
        fields = ['title', 'description', 'price', 'sku', 'quantity', 'cuisine']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}