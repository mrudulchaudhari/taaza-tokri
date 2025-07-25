from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplier_dashboard, name='supplier_dashboard'),
]
