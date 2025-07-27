# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUser(AbstractUser):
#     USER_TYPE_CHOICES = (
#         ('vendor', 'Vendor'),
#         ('supplier', 'Supplier'),
#         ('buyer', 'Buyer'),
#     )
#     user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = None  # removes username field
    USER_TYPE_CHOICES = (
        ('vendor', 'Vendor'),
        ('supplier', 'Supplier'),
        ('buyer', 'Buyer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
