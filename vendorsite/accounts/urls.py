from django.urls import path
from . import views

urlpatterns = [
    path('register/vendor/', views.register_vendor, name='register_vendor'),
    path('register/supplier/', views.register_supplier, name='register_supplier'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
