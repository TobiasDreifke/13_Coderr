from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from user_auth_app.models import UserProfile


class ProfileEndpointTests(APITestCase):
    """Verify profile detail and listing endpoint behavior."""

    def setUp(self):
        """Create business and customer users for profile endpoint tests."""
        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@example.com",
            password="securepass123",
            first_name="Biz",
            last_name="Owner",
        )
        UserProfile.objects.create(
            username=self.business_user,
            type="business",
            location="Berlin",
            tel="123456789",
            description="Business description",
            working_hours="9-17",
        )

        self.customer_user = User.objects.create_user(
            username="customer_user",
            email="customer@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=self.customer_user, type="customer")

    def authenticate(self, user):
        """Authenticate the test client as the given user."""
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_profile_detail_requires_authentication(self):
        """Ensure the profile detail endpoint requires authentication."""
        url = reverse("profile-detail", kwargs={"user_id": self.business_user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_returns_documented_blank_strings(self):
        """Ensure empty optional profile fields are returned as blank strings."""
        self.authenticate(self.customer_user)
        url = reverse("profile-detail", kwargs={"user_id": self.customer_user.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "")
        self.assertEqual(response.data["last_name"], "")
        self.assertEqual(response.data["location"], "")
        self.assertEqual(response.data["tel"], "")
        self.assertEqual(response.data["description"], "")
        self.assertEqual(response.data["working_hours"], "")

    def test_profile_patch_allows_owner_to_update_profile(self):
        """Ensure profile owners can update their own profile fields."""
        self.authenticate(self.business_user)
        url = reverse("profile-detail", kwargs={"user_id": self.business_user.id})

        response = self.client.patch(
            url,
            {
                "first_name": "Max",
                "last_name": "Mustermann",
                "location": "Hamburg",
                "tel": "987654321",
                "description": "Updated description",
                "working_hours": "10-18",
                "email": "updated_business@example.com",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.business_user.refresh_from_db()
        self.assertEqual(self.business_user.first_name, "Max")
        self.assertEqual(self.business_user.email, "updated_business@example.com")
        self.assertEqual(self.business_user.profile.location, "Hamburg")
        self.assertEqual(self.business_user.profile.working_hours, "10-18")

    def test_profile_patch_forbids_non_owner(self):
        """Ensure users cannot update someone else's profile."""
        self.authenticate(self.customer_user)
        url = reverse("profile-detail", kwargs={"user_id": self.business_user.id})

        response = self.client.patch(
            url,
            {"description": "Should not be updated"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_business_profiles_list_returns_only_business_users(self):
        """Ensure the business profile list excludes customer profiles."""
        self.authenticate(self.customer_user)
        url = reverse("business-profiles")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"], self.business_user.id)
        self.assertEqual(response.data[0]["type"], "business")

    def test_customer_profiles_list_returns_only_customer_users(self):
        """Ensure the customer profile list excludes business profiles."""
        self.authenticate(self.business_user)
        url = reverse("customer-profiles")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"], self.customer_user.id)
        self.assertEqual(response.data[0]["type"], "customer")
