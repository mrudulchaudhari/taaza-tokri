from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import VendorSignUpForm, SupplierSignUpForm
from .models import CustomUser

def register_vendor(request):
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('vendor_dashboard')
    else:
        form = VendorSignUpForm()
    return render(request, 'accounts/register_vendor.html', {'form': form})

def register_supplier(request):
    if request.method == 'POST':
        form = SupplierSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('supplier_dashboard')
    else:
        form = SupplierSignUpForm()
    return render(request, 'accounts/register_supplier.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'vendor':
                return redirect('vendor_dashboard')
            elif user.user_type == 'supplier':
                return redirect('supplier_dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
