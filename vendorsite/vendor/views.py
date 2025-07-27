from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from listings.models import ProductListing
from supplier.models import Order, OrderItem
from .models import Vendor

@login_required
def vendor_dashboard(request):
    try:
        vendor_profile = request.user.vendor_profile
    except Vendor.DoesNotExist:
        messages.error(request, "Your vendor profile could not be found.")
        return redirect('accounts:login')

    vendor_city = vendor_profile.city
    available_products = []

    if vendor_city:
        # This is the final, working query. It's case-insensitive.
        available_products = ProductListing.objects.filter(
            supplier__city__iexact=vendor_city,
            is_active=True,
            quantity__gt=0
        ).select_related('supplier')
    else:
        messages.warning(request, "Please set your city in your profile to see available products.")

    context = {
        'products': available_products,
        'vendor_city': vendor_city,
        'cart': request.session.get('cart', {})
    }
    return render(request, 'vendor/dashboard.html', context)

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            messages.error(request, "Please enter a valid quantity.")
            return redirect('vendor:dashboard')
        product = get_object_or_404(ProductListing, id=product_id)
        cart = request.session.get('cart', {})
        cart_item = cart.get(str(product_id), {'quantity': 0, 'price': str(product.price), 'title': product.title})
        cart_item['quantity'] += quantity
        if cart_item['quantity'] > product.quantity:
            messages.warning(request, f"Only {product.quantity} units of {product.title} are available.")
            cart_item['quantity'] = product.quantity
        cart[str(product_id)] = cart_item
        request.session['cart'] = cart
        messages.success(request, f"Added {quantity} x '{product.title}' to your cart.")
    return redirect('vendor:dashboard')

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())
    context = {'cart': cart, 'total_price': total_price}
    return render(request, 'vendor/cart.html', context)

@login_required
def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('vendor:view_cart')
    order = Order.objects.create(user=request.user, status='Pending')
    for product_id, item_data in cart.items():
        product = ProductListing.objects.get(id=int(product_id))
        OrderItem.objects.create(order=order, product=product, quantity=item_data['quantity'], price=item_data['price'])
    del request.session['cart']
    messages.success(request, "Your order has been placed successfully!")
    return redirect('vendor:dashboard')