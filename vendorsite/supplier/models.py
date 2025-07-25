from django.db import models

class MaterialCategory(models.Model):
    """
    Represents a category of raw materials that a supplier can provide.
    e.g., 'Vegetables', 'Spices', 'Dairy', 'Packaging'
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The name of the material category."
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Material Category"
        verbose_name_plural = "Material Categories"


class Supplier(models.Model):
    """
    Represents a supplier in the system, detailing their information.
    """
    name = models.CharField(max_length=255, help_text="The legal name of the supplier.")
    contact_person = models.CharField(max_length=255, blank=True, null=True, help_text="The primary contact person.")
    email = models.EmailField(unique=True, help_text="The supplier's primary email address.")
    phone = models.CharField(max_length=10, unique=True, help_text="The supplier's 10-digit phone number (used for login).")
    address = models.TextField(blank=True, null=True, help_text="The physical address of the supplier.")
    city = models.CharField(max_length=100, blank=True, null=True, help_text="The city where the supplier operates.")
    categories = models.ManyToManyField(
        MaterialCategory,
        blank=True,
        related_name="suppliers",
        help_text="Select the categories of materials this supplier provides."
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
