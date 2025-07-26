# accounts/views.py

from django.shortcuts import render, redirect
# IMPORT 'authenticate'
from django.contrib.auth import login, logout, authenticate
from .forms import VendorSignUpForm, SupplierSignUpForm
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# --- No changes to registration views ---
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


# --- UPDATED LOGIN VIEW TO HANDLE BOTH LOGINS ---
# accounts/views.py

def login_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'phone_login':
            phone = request.POST.get('phone')
            if not phone or not phone.isdigit() or len(phone) != 10:
                messages.error(request, "Please enter a valid 10-digit phone number.")
                return redirect('login')
            try:
                user = CustomUser.objects.get(phone=phone)
                login(request, user)
                
                # --- THIS IS THE CORRECTED LOGIC ---
                if user.user_type == 'vendor':
                    return redirect('vendor_dashboard')
                elif user.user_type == 'supplier':
                    return redirect('supplier_dashboard')
                elif user.user_type == 'buyer': # <-- THIS WAS MISSING
                    return redirect('buyer_dashboard') # <-- THIS WAS MISSING
                else:
                    # Fallback for other user types if needed
                    return redirect('login')

            except CustomUser.DoesNotExist:
                messages.error(request, "No user found with that phone number.")
                return redirect('login')

        elif action == 'superuser_login':
            # ... (your superuser login logic is correct and does not need changes)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_superuser:
                login(request, user)
                messages.success(request, "Superuser logged in successfully.")
                return redirect('/admin/')
            else:
                messages.error(request, "Invalid credentials or not a superuser.")
                return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def buyer_dashboard(request):
    # This view is for the buyer's main dashboard page.
    # In a real app, you would fetch real data from your database here.
    # For now, we'll use placeholder data.
    
    context = {
        'user': request.user,
        # Placeholder stats
        'order_count': 12,
        'total_spent': 8450,
        'rating': 4.8,
        'vendor_count': 15,
        # Placeholder recent activity
        'recent_activity': [
            {'icon': '📦', 'title': 'Order #1234 Delivered', 'description': 'Fresh vegetables from Fresh Foods Co.', 'time': '2 hours ago'},
            {'icon': '⭐', 'title': 'New Vendor Added', 'description': 'Spice Paradise is now available.', 'time': '1 day ago'},
            {'icon': '💰', 'title': 'Special Offer', 'description': 'Get 10% off on your next order.', 'time': '2 days ago'},
        ]
    }
    return render(request, 'accounts/buyer_dashboard.html', context)