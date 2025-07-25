from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_materials, name='list_materials'),
]