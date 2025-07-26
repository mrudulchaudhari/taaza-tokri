# File: listing/urls.py

from django.urls import path
from . import views

app_name = 'listing' # Set the app namespace

urlpatterns = [
    # Your original URL for the product list
    path('', views.list_materials, name='list_materials'),
    
    # URL for the cart page itself
    path('cart/', views.cart_detail, name='cart_detail'),
    
    # URLs for cart actions
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
]