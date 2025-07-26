# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from vendor.models import Vendor
from supplier.models import Supplier

class VendorSignUpForm(forms.ModelForm):
    # Add password fields which are not on the Vendor model but are needed for user creation
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Vendor
        # Specify the fields to include from the Vendor model
        fields = ['name', 'phone_number', 'email', 'city', 'address', 'cuisine']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email optional
        self.fields['email'].required = False
        # Make phone number read-only as it's pre-filled
        self.fields['phone_number'].widget.attrs['readonly'] = True

    def clean_confirm_password(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

    def save(self, commit=True):
        # Create the CustomUser instance
        user = CustomUser.objects.create_user(
            username=self.cleaned_data.get('phone_number'),
            password=self.cleaned_data.get('password'),
            user_type='vendor' # Set the user type
        )
        
        # Create the Vendor instance, linking it to the user
        vendor = super().save(commit=False)
        vendor.user = user
        
        if commit:
            vendor.save()
            
        return user


class SupplierSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'email', 'city', 'address', 'cuisine']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs['readonly'] = True

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            username=self.cleaned_data.get('phone'),
            password=self.cleaned_data.get('password'),
            user_type='supplier'
        )
        
        supplier = super().save(commit=False)
        supplier.user = user
        
        if commit:
            supplier.save()
            
        return user
