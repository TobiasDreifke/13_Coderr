from django.urls import path
from .views import BusinessProfilesListView, CustomerProfilesListView, ProfileDetailView

urlpatterns = [
   path('profile/<int:user_id>/', ProfileDetailView.as_view(), name='profile-detail'),
   path('profiles/business/', BusinessProfilesListView.as_view(), name='business-profiles'),
   path('profiles/customer/', CustomerProfilesListView.as_view(), name='customer-profiles'),
]
