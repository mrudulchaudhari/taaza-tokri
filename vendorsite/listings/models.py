from django.db import models

class ProductListing(models.Model):
    CUISINE_CHOICES = [
        ('CHAAT', 'Chaat'), ('PAV_BHAJI', 'Pav Bhaji'), ('SOUTH_INDIAN', 'South Indian'),
        ('CHOLE_BHATURE', 'Chole Bhature'), ('MOMOS', 'Momos'), ('NORTH_INDIAN', 'North Indian'),
        ('ROLLS', 'Rolls'), ('BIRYANI', 'Biryani'), ('SWEETS', 'Sweets'),
        ('BEVERAGES', 'Beverages'), ('OTHER', 'Other'),
    ]

    supplier = models.ForeignKey(
        'supplier.Supplier',
        on_delete=models.CASCADE,
        related_name='products'
    )
    vendor = models.ForeignKey(  # ✅ ADD THIS BACK!
        'vendor.Vendor',
        on_delete=models.CASCADE,
        related_name='product_listings'
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    cuisine = models.CharField(max_length=50, choices=CUISINE_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.supplier.name}"

    class Meta:
        unique_together = ('supplier', 'sku')
