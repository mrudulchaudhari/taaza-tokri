# listing/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# CHANGED: Import your actual model
from .models import ProductListing
from .cart import Cart

@login_required
def list_materials(request):
    # CHANGED: Query your ProductListing model and filter for active ones
    products = ProductListing.objects.filter(is_active=True)
    cart = Cart(request) # Pass cart to the template to show the correct count in the header
    return render(request, 'listings/list.html', {'products': products, 'cart': cart})

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'listing/cart.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    # CHANGED: Use your ProductListing model
    product = get_object_or_404(ProductListing, id=product_id)
    cart.add(product=product, quantity=1, update_quantity=False)
    return redirect('listing:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    # CHANGED: Use your ProductListing model
    product = get_object_or_404(ProductListing, id=product_id)
    cart.remove(product)
    return redirect('listing:cart_detail')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    # CHANGED: Use your ProductListing model
    product = get_object_or_404(ProductListing, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity, update_quantity=True)
    return redirect('listing:cart_detail')