from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import ProfileSerializer, BusinessProfileSerializer, CustomerProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        return User.objects.select_related('profile').all()

    def get_object(self):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(self.get_queryset(), id=user_id)

    def perform_update(self, serializer):
        if serializer.instance.id != self.request.user.id:
            raise PermissionDenied(
                "You do not have permission to edit this profile.")
        serializer.save()
        
class BusinessProfilesListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessProfileSerializer
    
    def get_queryset(self):
        return User.objects.select_related('profile').filter(profile__type='business')
    
class CustomerProfilesListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileSerializer
    
    def get_queryset(self):
        return User.objects.select_related('profile').filter(profile__type='customer')
    

        
