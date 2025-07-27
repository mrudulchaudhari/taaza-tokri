from django.urls import path
from . import views

app_name = 'supplier'

urlpatterns = [
    path('dashboard/', views.supplier_dashboard, name='dashboard'),
    path('order/<int:order_id>/update/<str:new_status>/', views.update_order_status, name='update_order_status'),
    path('order-history/', views.order_history, name='order_history'),
]