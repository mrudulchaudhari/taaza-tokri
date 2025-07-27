# vendorsite/supplier/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from listings.models import ProductListing
from .models import Order
from .forms import ProductListingForm

# vendorsite/supplier/views.py

@login_required
def supplier_dashboard(request):
    try:
        supplier_profile = request.user.supplier_profile
    except AttributeError:
        return redirect('some_other_page')  # or error page

    if request.method == 'POST':
        form = ProductListingForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.supplier = supplier_profile

            # ✅ ✅ ✅ Debug prints
            print("SUPPLIER:", supplier_profile)
            print("VENDOR:", supplier_profile.vendor)

            product.vendor = supplier_profile.vendor
            product.save()
            return redirect('supplier:dashboard')

    else:
        form = ProductListingForm()

    products = ProductListing.objects.filter(supplier=supplier_profile)
    pending_orders = Order.objects.filter(
        items__product__supplier=supplier_profile,
        status='Pending'
    ).distinct()

    context = {
        'form': form,
        'products': products,
        'pending_orders': pending_orders,
    }
    return render(request, 'supplier/dashboard.html', context)


@login_required
def update_order_status(request, order_id, new_status):
    valid_statuses = [status[0] for status in Order.STATUS_CHOICES]
    if new_status not in valid_statuses:
        return redirect('supplier:dashboard')

    order = get_object_or_404(
        Order,
        id=order_id,
        items__product__supplier=request.user.supplier_profile
    )
    order.status = new_status
    order.save()
    return redirect('supplier:dashboard')

@login_required
def order_history(request):
    past_orders = Order.objects.filter(
        items__product__supplier=request.user.supplier_profile
    ).exclude(
        Q(status='Pending') | Q(status='Processing')
    ).distinct().order_by('-created_at')

    context = { 'orders': past_orders }
    return render(request, 'supplier/order_history.html', context)