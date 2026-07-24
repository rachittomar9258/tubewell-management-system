from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('owner', 'Owner'),
        ('renter', 'Renter'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank = True, null = True)
    village = models.CharField(max_length = 100, blank= True, null= True)

    fast2sms_api_key = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.role})"