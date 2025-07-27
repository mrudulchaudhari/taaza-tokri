# listings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import ProductListing
from .cart import Cart
from supplier.models import Supplier

@login_required
def browse_all_products(request):
    """
    Main view for vendors to browse all products from all suppliers.
    Vendors browse products that SUPPLIERS are offering to sell to them.
    This is for vendors to find ingredients/supplies they need to purchase.
    """
    # Get all active products that suppliers are offering
    # These should be products that suppliers have listed for sale
    products = ProductListing.objects.filter(
        is_active=True,
        quantity__gt=0  # Only show products that are in stock
    ).select_related('supplier')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(supplier__name__icontains=search_query)
        )
    
    # Filter by cuisine
    cuisine_filter = request.GET.get('cuisine', '')
    if cuisine_filter:
        products = products.filter(cuisine=cuisine_filter)
    
    # Filter by supplier
    supplier_filter = request.GET.get('supplier', '')
    if supplier_filter:
        products = products.filter(supplier__id=supplier_filter)
    
    # Price range filter
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Sorting
    sort_by = request.GET.get('sort', 'title')
    valid_sorts = ['title', '-title', 'price', '-price', 'updated_at', '-updated_at', 'supplier__name', '-supplier__name']
    if sort_by in valid_sorts:
        products = products.order_by(sort_by)
    else:
        products = products.order_by('title')
    
    # Pagination
    paginator = Paginator(products, 20)  # 20 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all suppliers for filter dropdown
    from supplier.models import Supplier
    suppliers = Supplier.objects.filter(is_active=True).order_by('name')
    
    # Get cart
    cart = Cart(request)
    
    context = {
        'page_obj': page_obj,
        'products': page_obj,  # For template compatibility
        'cart': cart,
        'search_query': search_query,
        'cuisine_filter': cuisine_filter,
        'supplier_filter': supplier_filter,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'suppliers': suppliers,
        'cuisine_choices': ProductListing.CUISINE_CHOICES,
        'total_products': paginator.count,
    }
    
    return render(request, 'products.html', context)

@login_required
def list_materials(request):
    """
    Legacy view - now redirects to the main browse function
    """
    return redirect('listing:browse_all_products')

@login_required
def product_detail(request, product_id):
    """
    Detailed view of a single product
    """
    product = get_object_or_404(ProductListing, id=product_id, is_active=True)
    cart = Cart(request)
    
    # Get related products from the same supplier
    related_products = ProductListing.objects.filter(
        supplier=product.supplier,
        is_active=True
    ).exclude(id=product.id)[:5]
    
    context = {
        'product': product,
        'cart': cart,
        'related_products': related_products,
    }
    
    return render(request, 'product_detail.html', context)

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductListing, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity, update_quantity=False)
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

# Additional utility views
@login_required
def supplier_products(request, supplier_id):
    """
    View all products from a specific supplier
    """
    from supplier.models import Supplier
    supplier = get_object_or_404(Supplier, id=supplier_id, is_active=True)
    products = ProductListing.objects.filter(
        supplier=supplier,
        is_active=True
    ).order_by('title')
    
    # Pagination
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    cart = Cart(request)
    
    context = {
        'supplier': supplier,
        'page_obj': page_obj,
        'products': page_obj,
        'cart': cart,
    }
    
    return render(request, 'supplier_products.html', context)