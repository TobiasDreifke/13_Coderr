from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]

    username = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, default='customer')
