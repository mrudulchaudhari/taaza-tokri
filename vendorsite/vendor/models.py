from django.db import models

# Created by Purva Bhoyar

class Vendor(models.Model):
    """
    Represents a vendor in the system, storing their details.
    """
    name = models.CharField(max_length=255, help_text="The name of the vendor company.")
    contact_person = models.CharField(max_length=255, blank=True, null=True, help_text="The primary contact person at the vendor company.")
    email = models.EmailField(unique=True, help_text="The vendor's primary email address.")
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="The vendor's phone number.")
    address = models.TextField(blank=True, null=True, help_text="The physical address of the vendor.")
    is_active = models.BooleanField(default=True, help_text="Designates whether this vendor is active.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"
