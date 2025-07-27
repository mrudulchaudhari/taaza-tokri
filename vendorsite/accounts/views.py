# vendorsite/accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import VendorSignUpForm, SupplierSignUpForm, UserLoginForm
from vendor.models import Vendor
from supplier.models import Supplier

def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'supplier_profile'): return redirect('supplier:dashboard')
        elif hasattr(request.user, 'vendor_profile'): return redirect('vendor:dashboard')
        return redirect('home') # A fallback home page

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user = None
            try:
                user = Supplier.objects.get(phone=phone_number).user
            except Supplier.DoesNotExist:
                try:
                    user = Vendor.objects.get(phone_number=phone_number).user
                except Vendor.DoesNotExist:
                    pass

            if user:
                authenticated_user = authenticate(request, username=user.username, password=password)
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    if hasattr(authenticated_user, 'supplier_profile'): return redirect('supplier:dashboard')
                    elif hasattr(authenticated_user, 'vendor_profile'): return redirect('vendor:dashboard')
                    return redirect('home')
                else:
                    messages.error(request, "Incorrect password. Please try again.")
            else:
                messages.error(request, "No account found with this phone number.")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')

def signup_page_view(request):
    return render(request, 'signup.html')

def signup_start(request):
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        role = request.POST.get('role')
        if not role or not phone or not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Please enter a valid 10-digit phone number and select a role.")
            return redirect('accounts:signup_page')
        if Supplier.objects.filter(phone=phone).exists() or Vendor.objects.filter(phone_number=phone).exists():
            messages.warning(request, 'This phone number is already registered. Please log in.')
            return redirect('accounts:login')
        request.session['signup_phone'] = phone
        if role == 'buyer':
            return redirect('accounts:register_vendor')
        elif role == 'seller':
            return redirect('accounts:register_supplier')
    return redirect('accounts:signup_page')

def register_vendor(request):
    phone = request.session.get('signup_phone')
    if not phone:
        messages.error(request, 'Your session has expired. Please start over.')
        return redirect('accounts:signup_page')
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            del request.session['signup_phone']
            login(request, user)
            return redirect('vendor:dashboard')
    else:
        form = VendorSignUpForm(initial={'phone_number': phone})
    return render(request, 'accounts/register_vendor.html', {'form': form})

def register_supplier(request):
    phone = request.session.get('signup_phone')
    if not phone:
        messages.error(request, 'Your session has expired. Please start over.')
        return redirect('accounts:signup_page')
    if request.method == 'POST':
        form = SupplierSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            del request.session['signup_phone']
            login(request, user)
            return redirect('supplier:dashboard')
    else:
        form = SupplierSignUpForm(initial={'phone': phone})
    return render(request, 'accounts/register_supplier.html', {'form': form})

def home(request): # A simple homepage view
    return render(request, 'home.html')