from django.urls import path
from . import views

urlpatterns = [
    # Supplier Dashboard
    path('', views.supplier_dashboard, name='supplier_dashboard'),

    # Product Management
    path('products/', views.supplier_product_list, name='supplier_product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/update/<int:pk>/', views.update_product, name='update_product'),

    # Order Management
    path('orders/current/', views.supplier_current_orders, name='supplier_current_orders'),
    path('orders/history/', views.supplier_order_history, name='supplier_order_history'),
    path('orders/update_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
]