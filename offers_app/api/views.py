from rest_framework import permissions, generics
from ..models import OfferDetail, Offer
from .serializers import (
    OfferDetailSerializer, OfferSerializer,
    OfferListSerializer, OfferRetrieveSerializer, OfferUpdateSerializer
)
from .permissions import IsBusinessUser, IsOwner
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'p'


class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all().prefetch_related('details')
    pagination_class = LargeResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferSerializer
        return OfferListSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.AllowAny()]


class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all().prefetch_related('details')

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return OfferUpdateSerializer
        return OfferRetrieveSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsOwner()]


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
