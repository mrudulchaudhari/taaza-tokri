from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from listings.models import ProductListing
from django.db.models import Q
from .forms import ProductForm
from .models import Supplier, Order, OrderItem

@login_required
def supplier_dashboard(request):
    # Renders the main dashboard for the supplier.
    return render(request, 'supplier/dashboard.html') # CORRECTED: Changed template name for consistency

@login_required
def supplier_product_list(request):
    # Fetches and displays a list of products belonging to the logged-in supplier.
    supplier = get_object_or_404(Supplier, user=request.user)
    products = ProductListing.objects.filter(supplier=supplier)
    # CORRECTED: Rendering the correct template and passing 'products' in the context.
    return render(request, 'supplier/product_list.html', {'products': products}) 

@login_required
def add_product(request):
    # Handles the creation of a new product by the supplier.
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            supplier = get_object_or_404(Supplier, user=request.user)
            product.supplier = supplier
            product.save()
            return redirect('supplier_product_list')
    else:
        form = ProductForm()
    # CORRECTED: Rendering the correct template for adding a product.
    return render(request, 'supplier/add_product.html', {'form': form}) 

@login_required
def update_product(request, pk):
    # Handles updating an existing product's details.
    product = get_object_or_404(ProductListing, pk=pk, supplier__user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('supplier_product_list')
    else:
        form = ProductForm(instance=product)
    # CORRECTED: Rendering the correct template for updating a product.
    return render(request, 'supplier/update_product.html', {'form': form}) 

@login_required
def supplier_current_orders(request):
    """
    Display active orders containing products from the logged-in supplier.
    """
    supplier = get_object_or_404(Supplier, user=request.user)
    # Find order items linked to this supplier's products and filter for active orders
    order_items = OrderItem.objects.filter(
        product__supplier=supplier,
        order__status__in=['Pending', 'Processing']
    ).select_related('order', 'product').order_by('-order__created_at')

    # Get the unique orders from the order_items
    orders = sorted(list(set(item.order for item in order_items)), key=lambda order: order.created_at, reverse=True)
    
    return render(request, 'supplier/current_orders.html', {
        'orders': orders,
        'order_items': order_items
    })

@login_required
def supplier_order_history(request):
    """
    Display completed or cancelled orders for the logged-in supplier.
    """
    supplier = get_object_or_404(Supplier, user=request.user)
    # Find order items linked to this supplier's products and filter for past orders
    order_items = OrderItem.objects.filter(
        product__supplier=supplier,
        order__status__in=['Delivered', 'Cancelled'] # Use __in for cleaner filtering
    ).select_related('order', 'product').order_by('-order__created_at')
    
    # Get the unique orders from the order_items
    orders = sorted(list(set(item.order for item in order_items)), key=lambda order: order.created_at, reverse=True)

    # Pass both orders and order_items to the template
    return render(request, 'supplier/order_history.html', {
        'orders': orders,
        'order_items': order_items
    })

@login_required
def update_order_status(request, order_id):
    """
    Update the status of an order.
    """
    supplier = get_object_or_404(Supplier, user=request.user)
    order = get_object_or_404(Order, id=order_id)

    # Check if any product in the order belongs to the current supplier
    if not OrderItem.objects.filter(order=order, product__supplier=supplier).exists():
        # Handle unauthorized access by redirecting away
        return redirect('supplier_current_orders') 

    if request.method == 'POST':
        new_status = request.POST.get('status')
        # Only allow logical status updates
        if new_status in ['Processing', 'Shipped']: 
            order.status = new_status
            order.save()
    
    return redirect('supplier_current_orders')