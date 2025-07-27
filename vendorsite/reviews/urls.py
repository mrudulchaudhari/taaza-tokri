# reviews/urls.py
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('add/order/<int:order_id>/reviewee/<int:reviewee_id>/', views.add_review, name='add_review'),
    
    # ADD THIS LINE FOR THE NEW PAGE
    path('my-reviews/', views.user_reviews, name='user_reviews'),
]