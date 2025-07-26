from django.db import models

# Create your models here.


class Vendor(models.Model):
    """
    Represents a vendor in the system, storing their details.
    """

    # This list of choices has been added.
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

    name = models.CharField(max_length=255, help_text="The name of the vendor company.")
    contact_person = models.CharField(max_length=255, blank=True, null=True, help_text="The primary contact person at the vendor company.")
    email = models.EmailField(unique=True, help_text="The vendor's primary email address.")
    phone_number = models.CharField(max_length=10, unique=True, help_text="The vendor's 10-digit phone number (used for login).")
    address = models.TextField(blank=True, null=True, help_text="The physical address of the vendor.")
    city = models.CharField(max_length=100, blank=True, null=True, help_text="The city where the vendor operates.")

    cuisine = models.CharField(
        max_length=50,
        choices=CUISINE_CHOICES,
        blank=True,
        null=True,
        help_text="The primary type of food this vendor sells."
    )

    is_active = models.BooleanField(default=True, help_text="Designates whether this vendor is active.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Vendor"
        verbose_name_plural = "Sellers"