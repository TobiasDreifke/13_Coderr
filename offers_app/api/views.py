from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions
from rest_framework.pagination import PageNumberPagination

from ..models import Offer, OfferDetail
from .filters import OfferFilter
from .permissions import IsBusinessUser, IsOwner
from .serializers import (
    OfferDetailSerializer,
    OfferListSerializer,
    OfferRetrieveSerializer,
    OfferSerializer,
    OfferUpdateSerializer,
)


class LargeResultsSetPagination(PageNumberPagination):
    """Paginate offer lists with a configurable page size limit."""

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'


class OfferListCreateView(generics.ListCreateAPIView):
    """List offers publicly and allow business users to create new ones."""

    queryset = Offer.objects.all().prefetch_related('details')
    pagination_class = LargeResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['updated_at']

    def get_queryset(self):
        """Return distinct offers with prefetched detail variants."""
        return Offer.objects.all().prefetch_related('details').distinct()

    def get_serializer_class(self):
        """Choose the write serializer for POST and the list serializer otherwise."""
        if self.request.method == 'POST':
            return OfferSerializer
        return OfferListSerializer

    def get_permissions(self):
        """Require authentication and business profile ownership for creation."""
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.AllowAny()]


class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve an offer or allow its owner to update or delete it."""

    queryset = Offer.objects.all().prefetch_related('details')

    def get_serializer_class(self):
        """Use the update serializer for writes and the retrieve serializer for reads."""
        if self.request.method in ['PATCH', 'PUT']:
            return OfferUpdateSerializer
        return OfferRetrieveSerializer

    def get_permissions(self):
        """Allow authenticated reads and owner-only write access."""
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsOwner()]


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    """Retrieve a single offer detail variant."""

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
