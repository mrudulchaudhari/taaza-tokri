from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from listings.models import ProductListing
from .forms import ProductForm
from .models import Supplier

@login_required
def supplier_dashboard(request):
    return render(request, 'seller_dashboard.html')


@login_required
def supplier_product_list(request):
    supplier = get_object_or_404(Supplier, user=request.user)
    products = ProductListing.objects.filter(supplier=supplier)
    return render(request, 'seller_dashboard.html')


@login_required
def add_product(request):
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
    return render(request, 'seller_dashboard.html', {'form': form})


@login_required
def update_product(request, pk):
    product = get_object_or_404(ProductListing, pk=pk, supplier__user = request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('supplier_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'seller_dashboard.html', {'form': form})
