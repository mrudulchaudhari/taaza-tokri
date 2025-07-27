# FILE: vendor/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from listings.models import ProductListing
from supplier.models import Order, OrderItem
from .models import Vendor
from reviews.models import Review # <-- 1. ADDED THIS IMPORT

@login_required
def vendor_dashboard(request):
    """
    Displays the vendor dashboard with available products.
    THIS IS THE SIMPLIFIED VERSION: It shows all products from all cities.
    """
    try:
        # This part is still needed to make sure the user is a vendor
        vendor_profile = request.user.vendor_profile
    except Vendor.DoesNotExist:
        # If they don't have a vendor profile, they can't access this page.
        messages.error(request, "You do not have a vendor profile.")
        return redirect('accounts:login')

    # --- SIMPLIFIED CODE ---
    # This line now gets ALL active products with a quantity greater than 0.
    # The city filter has been removed for now.
    available_products = ProductListing.objects.filter(
        is_active=True,
        quantity__gt=0
    ).select_related('supplier')
    
    if not available_products.exists():
        messages.info(request, "No products are currently available from any supplier.")

    context = {
        'products': available_products,
        'cart': request.session.get('cart', {})
    }
    return render(request, 'vendor/dashboard.html', context)

@login_required
def order_history(request):
    # Your original query is kept, with 'reviews' added to prefetch_related
    orders = Order.objects.filter(user=request.user).prefetch_related(
        'items', 'items__product__supplier__user', 'reviews'
    ).order_by('-created_at')

    # 2. ADDED THIS LOOP to prepare data for the template
    for order in orders:
        order.is_reviewed_by_vendor = order.reviews.filter(reviewer=request.user).exists()
        review_from_supplier = order.reviews.filter(reviewee=request.user).first()
        order.review_from_supplier = review_from_supplier
        
    return render(request, 'vendor/order_history.html', {'orders': orders})

# --- The rest of your views are unchanged ---

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
    if not cart:
        return redirect('vendor:view_cart')
    
    order = Order.objects.create(user=request.user, status='Pending')
    for product_id, item_data in cart.items():
        product = ProductListing.objects.select_for_update().get(id=int(product_id))
        if product.quantity >= item_data['quantity']:
            OrderItem.objects.create(order=order, product=product, quantity=item_data['quantity'], price=item_data['price'])
            product.quantity -= item_data['quantity']
            product.save()
        else:
            messages.error(request, f"Not enough stock for {product.title}. Order cancelled.")
            return redirect('vendor:view_cart')

    del request.session['cart']
    messages.success(request, "Your order has been placed successfully!")
    return redirect('vendor:order_history')

@login_required
def mark_order_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'Shipped':
        order.status = 'Delivered'
        order.save()
        messages.success(request, f"Order #{order.id} has been marked as received.")
    else:
        messages.warning(request, f"Order #{order.id} could not be marked as received.")
        
    return redirect('vendor:order_history')