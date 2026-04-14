from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Store account type and public profile data for a user."""

    TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]

    username = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, default='customer')
    
    
    file = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, default='')
    tel = models.CharField(max_length=20, blank=True, default='' )
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Return a readable identifier for the related user profile."""
        return f"{self.username.username}'s profile"
