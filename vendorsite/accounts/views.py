# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import VendorSignUpForm, SupplierSignUpForm
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# --- CORRECTED: Import your actual profile models ---
from vendor.models import Vendor 
from supplier.models import Supplier

# --- View to display the signup page ---
def signup_page_view(request):
    """
    Renders the page where users select their role to begin registration.
    """
    return render(request, 'signup.html')


# --- CORRECTED: Handles the start of the signup process ---
def signup_start(request):
    """
    Checks if a user's phone number exists in the relevant profile model.
    - If yes, redirects to login.
    - If no, redirects to the appropriate detailed registration form.
    """
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')

        # --- Input validation ---
        if not role or role not in ['buyer', 'seller']:
            messages.error(request, "Please select a valid role.")
            return redirect('signup_page')

        if not phone_number or not phone_number.isdigit() or len(phone_number) != 10:
            messages.error(request, "Please enter a valid 10-digit phone number.")
            return redirect('signup_page')

        # --- Check if user already exists based on the selected role ---
        user_exists = False
        if role == 'buyer':
            # Check the Vendor model using the 'phone_number' field
            if Vendor.objects.filter(phone_number=phone_number).exists():
                user_exists = True
        elif role == 'seller':
            # Check the Supplier model using the 'phone' field
            if Supplier.objects.filter(phone=phone_number).exists():
                user_exists = True

        if user_exists:
            messages.warning(request, 'This phone number is already registered. Please log in.')
            return redirect('login') 

        # --- If user is new, store info in session and redirect ---
        request.session['signup_phone'] = phone_number
        
        if role == 'buyer':
            return redirect('register_vendor')
        elif role == 'seller':
            return redirect('register_supplier')

    return redirect('signup_page')


# --- CORRECTED: To pre-fill phone number from session ---
def register_vendor(request):
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST)
        if form.is_valid():
            # The form's save() method should handle creating the user and profile
            user = form.save()
            
            if 'signup_phone' in request.session:
                del request.session['signup_phone']
            login(request, user)
            return redirect('vendor_dashboard') # Or 'buyer_dashboard'
    else:
        phone = request.session.get('signup_phone')
        if not phone:
            messages.error(request, 'Please start the registration process from the beginning.')
            return redirect('signup_page')
        # Use 'phone_number' to match the Vendor model field
        form = VendorSignUpForm(initial={'phone_number': phone})
        
    return render(request, 'accounts/register_vendor.html', {'form': form})


# --- CORRECTED: To pre-fill phone number from session ---
def register_supplier(request):
    if request.method == 'POST':
        form = SupplierSignUpForm(request.POST)
        if form.is_valid():
            # The form's save() method should handle creating the user and profile
            user = form.save()
            
            if 'signup_phone' in request.session:
                del request.session['signup_phone']
            login(request, user)
            return redirect('supplier_dashboard')
    else:
        phone = request.session.get('signup_phone')
        if not phone:
            messages.error(request, 'Please start the registration process from the beginning.')
            return redirect('signup_page')
        # Use 'phone' to match the Supplier model field
        form = SupplierSignUpForm(initial={'phone': phone})
        
    return render(request, 'accounts/register_supplier.html', {'form': form})


# --- Your existing login and other views remain unchanged ---

def login_view(request):
    # Note: This login view will also need to be updated to check 
    # the Vendor and Supplier models to find the user by phone number.
    if request.method == 'POST':
        # ... (your existing login logic)
        pass
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def buyer_dashboard(request):
    # ... (your existing dashboard logic)
    pass
