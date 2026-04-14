from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Review
from .serializers import ReviewSerializer, ReviewUpdateSerializer
from .permissions import IsCustomerUser, IsReviewOwner
from .filters import ReviewFilter


class ReviewListCreateView(generics.ListCreateAPIView):
    """List reviews and allow authenticated customers to create them."""

    queryset = Review.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at']

    def get_serializer_class(self):
        """Return the serializer used for listing and creating reviews."""
        if self.request.method == 'POST':
            return ReviewSerializer
        return ReviewSerializer

    def get_permissions(self):
        """Apply customer-only permissions to review creation requests."""
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        return [permissions.IsAuthenticated()]


class ReviewUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a review owned by the requester."""

    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsReviewOwner]

    def get_serializer_class(self):
        """Use the update serializer for writes and the default serializer otherwise."""
        if self.request.method in ['PATCH', 'PUT']:
            return ReviewUpdateSerializer
        return ReviewSerializer
