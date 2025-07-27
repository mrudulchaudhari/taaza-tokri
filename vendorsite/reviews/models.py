# reviews/models.py (FIXED VERSION)

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count

class Review(models.Model):
    REVIEWER_TYPES = [
        ('vendor', 'Vendor'),
        ('supplier', 'Supplier'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Use settings.AUTH_USER_MODEL instead of User
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_reviews')
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_reviews')
    reviewer_type = models.CharField(max_length=10, choices=REVIEWER_TYPES)
    reviewee_type = models.CharField(max_length=10, choices=REVIEWER_TYPES)
    
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='approved')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['reviewer', 'reviewee', 'order_id']
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.reviewer.username} -> {self.reviewee.username} ({self.rating}/5)'
    
    @staticmethod
    def get_user_stats(user, user_type):
        reviews = Review.objects.filter(reviewee=user, reviewee_type=user_type, status='approved')
        
        if not reviews.exists():
            return {
                'total_reviews': 0,
                'average_rating': 0,
                'rating_distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            }
        
        stats = reviews.aggregate(
            total_reviews=Count('id'),
            average_rating=Avg('rating')
        )
        
        rating_distribution = {}
        for i in range(1, 6):
            rating_distribution[i] = reviews.filter(rating=i).count()
        
        stats['rating_distribution'] = rating_distribution
        stats['average_rating'] = round(stats['average_rating'], 1) if stats['average_rating'] else 0
        
        return stats


class ReviewResponse(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='response')
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Fixed
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Response by {self.responder.username}'


class ReviewHelpful(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='helpful_votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Fixed
    user_type = models.CharField(max_length=10, choices=Review.REVIEWER_TYPES)
    is_helpful = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['review', 'user']
    
    def __str__(self):
        return f'{self.user.username} found review #{self.review.id} {"helpful" if self.is_helpful else "not helpful"}'