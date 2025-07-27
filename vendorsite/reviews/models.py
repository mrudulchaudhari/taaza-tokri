# reviews/models.py
from django.db import models
from django.conf import settings
from supplier.models import Order 

class Review(models.Model):
    # The order this review is associated with.
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews')
    
    # The user who is writing the review.
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_reviews')
    
    # The user who is being reviewed.
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_reviews')
    
    # A rating from 1 to 5 stars.
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user can only review another user once per order.
        unique_together = ('order', 'reviewer', 'reviewee')
        ordering = ['-created_at']

    def __str__(self):
        return f'Review of {self.reviewee.email} by {self.reviewer.email} for Order #{self.order.id}'