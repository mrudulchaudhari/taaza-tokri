from django.urls import path
from . import views

app_name = 'vendor'

urlpatterns = [
    path('dashboard/', views.vendor_dashboard, name='dashboard'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/place-order/', views.place_order, name='place_order'),
    path('orders/', views.order_history, name='order_history'),
    path('order/<int:order_id>/mark-delivered/', views.mark_order_delivered, name='mark_delivered'),
]