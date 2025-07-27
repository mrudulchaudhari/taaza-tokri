from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from listings.models import ProductListing
from supplier.models import Order, OrderItem
from .models import Vendor

@login_required
def vendor_dashboard(request):
    try: vendor_profile = request.user.vendor_profile
    except Vendor.DoesNotExist: return redirect('accounts:login')
    vendor_city = vendor_profile.city
    available_products = []
    if vendor_city:
        available_products = ProductListing.objects.filter(supplier__city__iexact=vendor_city, is_active=True, quantity__gt=0).select_related('supplier')
    else: messages.warning(request, "Please set your city in your profile to see products.")
    context = {'products': available_products, 'vendor_city': vendor_city, 'cart': request.session.get('cart', {})}
    return render(request, 'vendor/dashboard.html', context)

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
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
    return render(request, 'vendor/cart.html', {'cart': cart, 'total_price': total_price})

@login_required
@transaction.atomic
def place_order(request):
    cart = request.session.get('cart', {})
    if not cart: return redirect('vendor:view_cart')
    
    order = Order.objects.create(user=request.user, status='Pending')
    for product_id, item_data in cart.items():
        # Lock the product row to prevent race conditions
        product = ProductListing.objects.select_for_update().get(id=int(product_id))
        if product.quantity >= item_data['quantity']:
            OrderItem.objects.create(order=order, product=product, quantity=item_data['quantity'], price=item_data['price'])
            # Reduce the quantity
            product.quantity -= item_data['quantity']
            product.save()
        else:
            messages.error(request, f"Not enough stock for {product.title}. Order cancelled.")
            # This will roll back the entire transaction, including the Order creation.
            return redirect('vendor:view_cart')

    del request.session['cart']
    messages.success(request, "Your order has been placed successfully!")
    return redirect('vendor:order_history')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items', 'items__product', 'items__product__supplier').order_by('-created_at')
    return render(request, 'vendor/order_history.html', {'orders': orders})

@login_required
def mark_order_delivered(request, order_id):
    """
    Allows the vendor to mark an order they placed as 'Delivered'.
    """
    # Get the order, ensuring it belongs to the logged-in user
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Only allow this action if the order is currently 'Shipped'
    if order.status == 'Shipped':
        order.status = 'Delivered'
        order.save()
        messages.success(request, f"Order #{order.id} has been marked as received.")
    else:
        messages.warning(request, f"Order #{order.id} could not be marked as received.")
        
    return redirect('vendor:order_history')