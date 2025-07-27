# vendorsite/supplier/models.py

from django.db import models
from django.conf import settings
from listings.models import ProductListing

# NOTE: The import for Vendor has been removed.

class Supplier(models.Model):
    """
    Represents a supplier in the system. The direct link to a Vendor is removed.
    """
    CUISINE_CHOICES = [
        ('CHAAT', 'Chaat'), ('PAV_BHAJI', 'Pav Bhaji'), ('SOUTH_INDIAN', 'South Indian'),
        ('CHOLE_BHATURE', 'Chole Bhature'), ('MOMOS', 'Momos'), ('NORTH_INDIAN', 'North Indian'),
        ('ROLLS', 'Rolls'), ('BIRYANI', 'Biryani'), ('SWEETS', 'Sweets'),
        ('BEVERAGES', 'Beverages'), ('OTHER', 'Other'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='supplier_profile'
    )
    
    # REMOVED: The ForeignKey to Vendor is gone, as requested.
    # vendor = models.ForeignKey(Vendor, ...)

    name = models.CharField(max_length=255, help_text="The legal name of the supplier.")
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    cuisine = models.CharField(max_length=50, choices=CUISINE_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    # This model correctly links a User (who could be a Vendor) to an order.
    # No changes are needed here.
    STATUS_CHOICES = (
        ('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    # This model is also correct. It links an order to a specific product listing.
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductListing, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"