from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('add/<int:user_id>/', views.add_review, name='add_review'),
    path('user/<int:user_id>/', views.user_reviews, name='user_reviews'),
    path('response/<int:review_id>/', views.add_review_response, name='add_review_response'),
    path('helpful/<int:review_id>/', views.mark_review_helpful, name='mark_review_helpful'),
    path('api/stats/<int:user_id>/', views.api_user_stats, name='api_user_stats'),
]