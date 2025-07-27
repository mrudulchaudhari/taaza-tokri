from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from vendor.models import Vendor
from supplier.models import Supplier

# --- Login Form (This form is correct) ---
class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label="Phone Number", max_length=10, widget=forms.TextInput(attrs={'id': 'phone'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


# --- Vendor Signup Form (Corrected) ---
class VendorSignUpForm(UserCreationForm):
    # These fields are for the Vendor's profile information
    shop_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # These are the fields for the main user account
        fields = ('username',)

    def save(self, commit=True):
        # This now correctly saves the user and their hashed password first
        user = super().save(commit=True)
        # Then it creates the linked Vendor profile
        Vendor.objects.create(
            user=user,
            shop_name=self.cleaned_data['shop_name'],
            phone_number=self.cleaned_data['phone_number'],
            address=self.cleaned_data.get('address', '')
        )
        return user


# --- Supplier Signup Form (Corrected) ---
# vendorsite/accounts/forms.py

class SupplierSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True, label="Full Name or Business Name")
    phone = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.EmailField(required=True)
    address = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.CharField(max_length=100, required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username',)

    def save(self, commit=True):
        user = super().save(commit=True)
        
        # ✅ IMPORTANT: pick an actual Vendor
        # Here: just take the first one — adapt as you wish!
        vendor = Vendor.objects.first()
        if not vendor:
            raise ValueError("No Vendor found! Please create at least one Vendor before registering Suppliers.")
        
        Supplier.objects.create(
            user=user,
            vendor=vendor,  # ✅ REQUIRED
            name=self.cleaned_data['name'],
            phone=self.cleaned_data['phone'],
            email=self.cleaned_data['email'],
            address=self.cleaned_data.get('address', ''),
            city=self.cleaned_data.get('city', ''),
            # Replace: your form should collect email too!
        )
        return user
