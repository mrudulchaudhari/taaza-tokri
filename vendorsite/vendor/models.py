from django.db import models

class Cuisine(models.Model):
    """
    Represents a type of cuisine or food category that a vendor can sell.
    e.g., 'Chaat', 'South Indian', 'Momos'
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The name of the cuisine category."
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Cuisine"
        verbose_name_plural = "Cuisines"


class Vendor(models.Model):
    """
    Represents a vendor in the system, storing their details.
    """
    name = models.CharField(max_length=255, help_text="The name of the vendor company.")
    contact_person = models.CharField(max_length=255, blank=True, null=True, help_text="The primary contact person at the vendor company.")
    email = models.EmailField(unique=True, help_text="The vendor's primary email address.")
    phone_number = models.CharField(max_length=10, unique=True, help_text="The vendor's 10-digit phone number (used for login).")
    address = models.TextField(blank=True, null=True, help_text="The physical address of the vendor.")
    city = models.CharField(max_length=100, blank=True, null=True, help_text="The city where the vendor operates.")
    cuisines = models.ManyToManyField(
        Cuisine,
        blank=True,
        related_name="vendors",
        help_text="Select the types of food this vendor sells."
    )
    is_active = models.BooleanField(default=True, help_text="Designates whether this vendor is active.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"
