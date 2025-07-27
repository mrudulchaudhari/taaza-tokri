# listings/urls.py
from django.urls import path
from . import views

app_name = 'listing'

urlpatterns = [
    # Main product browsing (this is the core functionality for issue #21)
    path('', views.browse_all_products, name='browse_all_products'),
    path('browse/', views.browse_all_products, name='browse_all_products'),
    path('products/', views.browse_all_products, name='products'),  # Match your existing URL
    
    # Legacy URL - redirects to main browse
    path('materials/', views.list_materials, name='list_materials'),
    
    # Product detail
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Supplier-specific products
    path('supplier/<int:supplier_id>/products/', views.supplier_products, name='supplier_products'),
    
    # Cart functionality
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
]