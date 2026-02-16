from rest_framework import generics, permissions, filters
# from django_filters.rest_framework import DjangoFilterBackend
from ..models import Review
from .serializers import ReviewSerializer, ReviewUpdateSerializer
from .permissions import IsCustomerUser, IsReviewOwner


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    filter_backends = [ filters.OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewSerializer
        return ReviewSerializer  

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        return [permissions.IsAuthenticated()]


class ReviewUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsReviewOwner]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return ReviewUpdateSerializer
        return ReviewSerializer