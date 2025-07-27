from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_page_view, name='signup_page'),
    path('signup/start/', views.signup_start, name='signup_start'),
    path('register/vendor/', views.register_vendor, name='register_vendor'),
    path('register/supplier/', views.register_supplier, name='register_supplier'),
]