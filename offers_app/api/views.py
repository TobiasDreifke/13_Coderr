from rest_framework import viewsets, status, permissions, generics
from ..models import Offer, OfferDetail
from .serializers import (
    OfferDetailSerializer
)

class OfferDetailViewSet(generics.ListCreateAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]