from rest_framework import viewsets, status, permissions, generics
from ..models import OfferDetail, Offer
from .serializers import (
    OfferDetailSerializer
)

class OfferDetailViewSet(generics.ListCreateAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]