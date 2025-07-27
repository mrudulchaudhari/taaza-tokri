from django.urls import path
from . import views


app_name = 'vendor'
urlpatterns = [
    path('vendor/', views.vendor_dashboard, name='vendor_dashboard'),
]
