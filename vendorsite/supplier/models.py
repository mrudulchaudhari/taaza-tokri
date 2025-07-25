from django.db import models

# Created by Purva Bhoyar

class Supplier(models.Model):
    """
    Represents a supplier in the system, detailing their information.
    """
    name = models.CharField(max_length=255, help_text="The legal name of the supplier.")
    contact_person = models.CharField(max_length=255, blank=True, null=True, help_text="The primary contact person.")
    email = models.EmailField(unique=True, help_text="The supplier's primary email address.")
    phone = models.CharField(max_length=25, blank=True, null=True, help_text="The supplier's phone number.")
    address = models.TextField(blank=True, null=True, help_text="The physical address of the supplier.")
    product_category = models.CharField(max_length=100, blank=True, null=True, help_text="The main category of products supplied.")
    is_active = models.BooleanField(default=True, help_text="Designates whether this supplier is active.")
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
