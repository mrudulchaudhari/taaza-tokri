from django.db import models
from django.conf import settings  # to reference AUTH_USER_MODEL
from listings.models import ProductListing

class Supplier(models.Model):
    """
    Represents a supplier in the system, detailing their information.
    """

    CUISINE_CHOICES = [
        ('CHAAT', 'Chaat'),
        ('PAV_BHAJI', 'Pav Bhaji'),
        ('SOUTH_INDIAN', 'South Indian'),
        ('CHOLE_BHATURE', 'Chole Bhature'),
        ('MOMOS', 'Momos'),
        ('NORTH_INDIAN', 'North Indian'),
        ('ROLLS', 'Rolls'),
        ('BIRYANI', 'Biryani'),
        ('SWEETS', 'Sweets'),
        ('BEVERAGES', 'Beverages'),
        ('OTHER', 'Other'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='supplier_profile',
        help_text="Link to the user profile for this supplier."
    )

    name = models.CharField(max_length=255, help_text="The legal name of the supplier.")
    contact_person = models.CharField(max_length=255, blank=True, null=True, help_text="The primary contact person.")
    email = models.EmailField(unique=True, help_text="The supplier's primary email address.")
    phone = models.CharField(max_length=10, unique=True, help_text="The supplier's 10-digit phone number (used for login).")
    address = models.TextField(blank=True, null=True, help_text="The physical address of the supplier.")
    city = models.CharField(max_length=100, blank=True, null=True, help_text="The city where the supplier operates.")

    cuisine = models.CharField(
        max_length=50,
        choices=CUISINE_CHOICES,
        blank=True,
        null=True,
        help_text="The main cuisine or food category this supplier provides ingredients for."
    )

    is_active = models.BooleanField(default=True, help_text="Designates whether this supplier is active.")
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'), 
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, '')
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductListing, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.title} in Order #{self.order.id}"