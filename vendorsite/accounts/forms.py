# vendorsite/accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from vendor.models import Vendor
from supplier.models import Supplier

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label="Phone Number", max_length=10, widget=forms.TextInput(attrs={'id': 'phone'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class VendorSignUpForm(UserCreationForm):
    shop_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    address = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username',)

    def save(self, commit=True):
        user = super().save(commit=True)
        Vendor.objects.create(
            user=user,
            shop_name=self.cleaned_data['shop_name'],
            phone_number=self.cleaned_data['phone_number'],
            address=self.cleaned_data.get('address', ''),
            city=self.cleaned_data.get('city', '')
        )
        return user

class SupplierSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True, label="Full Name or Business Name")
    phone = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    address = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username',)

    def save(self, commit=True):
        user = super().save(commit=True)
        Supplier.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            phone=self.cleaned_data['phone'],
            address=self.cleaned_data.get('address', ''),
            city=self.cleaned_data.get('city', '')
        )
        return user