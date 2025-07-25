from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class VendorSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'vendor'
        if commit:
            user.save()
        return user

class SupplierSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'supplier'
        if commit:
            user.save()
        return user
