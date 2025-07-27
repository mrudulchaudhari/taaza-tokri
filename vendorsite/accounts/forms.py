from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from vendor.models import Vendor
from supplier.models import Supplier

# --- Login Form (This is correct) ---
class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label="Phone Number", max_length=10, widget=forms.TextInput(attrs={'id': 'phone'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

# --- Vendor Signup Form (This is also correct) ---
class VendorSignUpForm(UserCreationForm):
    shop_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    address = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email') # Email for the main user account

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

# --- Supplier Signup Form (CORRECTED) ---
class SupplierSignUpForm(UserCreationForm):
    # These fields are for the Supplier's profile information
    name = forms.CharField(max_length=255, required=True, label="Full Name or Business Name")
    phone = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    address = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.CharField(max_length=100, required=True)
    
    # THIS IS THE FIX: We explicitly ask for the email here again to ensure it's passed to the Supplier model.
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # We handle the email field ourselves, so we only need the username from the base form.
        fields = ('username',)

    def save(self, commit=True):
        user = super().save(commit=False)
        # We take the email from our form and assign it to the user object before saving.
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # We now pass the same email to the Supplier profile, satisfying the UNIQUE constraint.
            Supplier.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                phone=self.cleaned_data['phone'],
                email=self.cleaned_data['email'],
                address=self.cleaned_data.get('address', ''),
                city=self.cleaned_data.get('city', '')
            )
        return user