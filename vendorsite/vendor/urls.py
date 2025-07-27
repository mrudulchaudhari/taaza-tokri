from django.urls import path
from . import views

urlpatterns = [
    path('vendor/', views.vendor_dashboard, name='vendor_dashboard'),
    path('dashboard/', views.dashboard, name='vendor_dashboard'),
    path('', views.dashboard, name='vendor_dashboard'),
]
