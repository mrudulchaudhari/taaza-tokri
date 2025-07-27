from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import CustomUser
from vendor.models import Vendor
from supplier.models import Supplier

class UserLoginForm(forms.Form):
    # This form is likely used for login, but it's not the cause of the error.
    phone_number = forms.CharField(label="Phone Number", max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)

class VendorSignUpForm(UserCreationForm):
    # These are the extra fields for the Vendor profile
    shop_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # CORRECTED: Use 'email' and other existing fields, NOT 'username'.
        # UserCreationForm handles the password fields automatically.
        fields = ('email', 'first_name', 'last_name')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'vendor' # Set the user type
        if commit:
            user.save()
        
        # Create the related Vendor profile
        Vendor.objects.create(
            user=user, 
            shop_name=self.cleaned_data['shop_name'], 
            phone_number=self.cleaned_data['phone_number'], 
            address=self.cleaned_data.get('address', ''), 
            city=self.cleaned_data.get('city', '')
        )
        return user

class SupplierSignUpForm(UserCreationForm):
    # Extra fields for the Supplier profile
    name = forms.CharField(max_length=255, required=True, label="Full Name or Business Name")
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # CORRECTED: Use 'email' and other existing fields, NOT 'username'.
        fields = ('email', 'first_name', 'last_name')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'supplier' # Set the user type
        if commit:
            user.save()
            
        # Create the related Supplier profile
        Supplier.objects.create(
            user=user, 
            name=self.cleaned_data['name'], 
            phone=self.cleaned_data['phone'], 
            address=self.cleaned_data.get('address', ''), 
            city=self.cleaned_data.get('city', '')
        )
        return user
