from django.db import models
from django.conf import settings

class Offer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='offers'
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class OfferDetail(models.Model):
    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    
    offer = models.ForeignKey(
        Offer, 
        on_delete=models.CASCADE,
        related_name='details'
    )
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()  
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPE_CHOICES)
    
    class Meta:
        unique_together = ['offer', 'offer_type'] 
    
    def __str__(self):
        return f"{self.offer.title} - {self.offer_type}"