from rest_framework import permissions, generics
from ..models import OfferDetail, Offer
from .serializers import (
    OfferDetailSerializer, OfferSerializer, OfferListSerializer, OfferRetrieveSerializer
)


class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all().prefetch_related('details')
    serializer_class = OfferRetrieveSerializer  
    permission_classes = [permissions.IsAuthenticated]


class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all().prefetch_related('details')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferSerializer    
        return OfferListSerializer

class OfferDetailRetrieveView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer  
    permission_classes = [permissions.IsAuthenticated]