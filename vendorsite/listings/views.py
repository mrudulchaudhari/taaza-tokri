# listings/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import ProductListing
from .cart import Cart

@login_required
def list_materials(request):
    products = ProductListing.objects.filter(is_active=True)
    cart = Cart(request)
    # CORRECTED PATH: Removed the 'listings/' prefix
    return render(request, 'list.html', {'products': products, 'cart': cart})

def cart_detail(request):
    cart = Cart(request)
    # CORRECTED PATH: Removed the 'listings/' prefix
    return render(request, 'cart.html', {'cart': cart})

# --- No changes are needed for the functions below ---

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductListing, id=product_id)
    cart.add(product=product, quantity=1, update_quantity=False)
    return redirect('listing:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductListing, id=product_id)
    cart.remove(product)
    return redirect('listing:cart_detail')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductListing, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity, update_quantity=True)
    return redirect('listing:cart_detail')