from django.urls import path
from .views import OfferDetailViewSet

urlpatterns = [
   path('offers/', OfferDetailViewSet.as_view(), name='offer-list-create'),
]
