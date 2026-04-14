from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import ProfileSerializer, BusinessProfileSerializer, CustomerProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve a single profile and allow the owner to update it."""

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        """Return users with their related profile loaded eagerly."""
        return User.objects.select_related('profile').all()

    def get_object(self):
        """Fetch the requested user profile by URL parameter."""
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(self.get_queryset(), id=user_id)

    def perform_update(self, serializer):
        """Prevent users from editing profiles that do not belong to them."""
        if serializer.instance.id != self.request.user.id:
            raise PermissionDenied(
                "You do not have permission to edit this profile.")
        serializer.save()


class BusinessProfilesListView(generics.ListAPIView):
    """List all users whose profile type is business."""

    permission_classes = [IsAuthenticated]
    serializer_class = BusinessProfileSerializer

    def get_queryset(self):
        """Return business users with related profile data."""
        return User.objects.select_related('profile').filter(profile__type='business')


class CustomerProfilesListView(generics.ListAPIView):
    """List all users whose profile type is customer."""

    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileSerializer

    def get_queryset(self):
        """Return customer users with related profile data."""
        return User.objects.select_related('profile').filter(profile__type='customer')
