from django.db import models
from vendor.models import Vendor
from supplier.models import Supplier

class ProductListing(models.Model):
    """
    Represents a product listing in the system.
    Each listing is associated with a vendor and optionally a supplier.
    """
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name='listings',
        help_text="The vendor for this listing."
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='listings',
        help_text="The supplier for this product."
    )
    title = models.CharField(max_length=255, help_text="The title of the product listing.")
    description = models.TextField(blank=True, null=True, help_text="A description for the product.")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="The price of the product.")
    sku = models.CharField(max_length=100, unique=True, help_text="Stock Keeping Unit.")
    quantity = models.PositiveIntegerField(default=0, help_text="Available stock quantity.")
    is_active = models.BooleanField(default=True, help_text="Is this listing active and visible?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} ({self.sku})"

    class Meta:
        ordering = ['-updated_at']
        unique_together = ('vendor', 'sku')
        verbose_name = "Product Listing"
        verbose_name_plural = "Product Listings"
