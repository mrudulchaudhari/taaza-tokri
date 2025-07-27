
# ----------------------------------------------------
# FILE: supplier/views.py
# ----------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from listings.models import ProductListing
from .models import Order
from .forms import ProductListingForm
from reviews.models import Review # <-- This import is added

# --- THIS VIEW IS UPDATED TO SUPPORT REVIEWS ---
@login_required
def supplier_dashboard(request):
    try:
        supplier_profile = request.user.supplier_profile
    except AttributeError:
        return redirect('accounts:login')

    if request.method == 'POST':
        form = ProductListingForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.supplier = supplier_profile
            product.save()
            return redirect('supplier:dashboard')
    else:
        form = ProductListingForm()

    products = ProductListing.objects.filter(supplier=supplier_profile)
    pending_orders = Order.objects.filter(items__product__supplier=supplier_profile, status='Pending').distinct()
    completed_orders = Order.objects.filter(items__product__supplier=supplier_profile).exclude(status='Pending').distinct().prefetch_related('reviews')
    
    for order in completed_orders:
        # Check if the supplier has already reviewed the vendor for this order
        order.is_reviewed_by_supplier = order.reviews.filter(reviewer=request.user).exists()
        
        # Find the review given BY the vendor TO the supplier for this order
        review_from_vendor = order.reviews.filter(reviewee=request.user).first()
        order.review_from_vendor = review_from_vendor
        
    context = {'form': form, 'products': products, 'pending_orders': pending_orders, 'completed_orders': completed_orders}
    return render(request, 'supplier/dashboard.html', context)

# This view is correct. No changes needed.
@login_required
def update_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id, items__product__supplier=request.user.supplier_profile)
    if new_status in ['Shipped', 'Cancelled']:
        order.status = new_status
        order.save()
    return redirect('supplier:dashboard')

# --- THIS VIEW IS UPDATED TO SUPPORT REVIEWS ---
@login_required
def order_history(request):
    orders = Order.objects.filter(items__product__supplier=request.user.supplier_profile).exclude(status='Pending').distinct().order_by('-created_at').prefetch_related('reviews')
    
    for order in orders:
        # Check if the supplier has already reviewed the vendor for this order
        order.is_reviewed_by_supplier = order.reviews.filter(reviewer=request.user).exists()

        # Find the review given BY the vendor TO the supplier for this order
        review_from_vendor = order.reviews.filter(reviewee=request.user).first()
        order.review_from_vendor = review_from_vendor
        
    return render(request, 'supplier/order_history.html', {'orders': orders})