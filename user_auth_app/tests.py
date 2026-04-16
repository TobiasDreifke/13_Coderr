from django.contrib.auth.models import User
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer
from orders_app.models import Order
from reviews_app.models import Review
from user_auth_app.models import UserProfile


class AuthenticationTests(APITestCase):
    """Cover registration and login behavior for token authentication."""

    def test_guest_users_exist_with_expected_profiles(self):
        """Ensure the seeded guest accounts are present in fresh databases."""
        customer_user = User.objects.get(username="andrey")
        business_user = User.objects.get(username="kevin")

        self.assertTrue(customer_user.check_password("asdasd"))
        self.assertEqual(customer_user.profile.type, "customer")

        self.assertTrue(business_user.check_password("asdasd24"))
        self.assertEqual(business_user.profile.type, "business")

    def test_seed_demo_content_creates_demo_data_idempotently(self):
        """Ensure the demo seed command creates stable sample data."""
        call_command("seed_demo_content")
        call_command("seed_demo_content")

        self.assertTrue(User.objects.filter(username="sophie_seo").exists())
        self.assertEqual(Offer.objects.count(), 4)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Review.objects.count(), 4)

    def test_registration_creates_user_profile_and_returns_token(self):
        """Ensure registration creates both the user profile and auth token."""
        url = reverse("register")
        payload = {
            "username": "new_customer",
            "email": "new_customer@example.com",
            "password": "securepass123",
            "repeated_password": "securepass123",
            "type": "customer",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertTrue(Token.objects.filter(user__username="new_customer").exists())

        user = User.objects.get(username="new_customer")
        self.assertEqual(user.email, payload["email"])
        self.assertEqual(user.profile.type, "customer")
        self.assertEqual(response.data["user_id"], user.id)

    def test_registration_rejects_mismatched_passwords(self):
        """Ensure registration fails when password confirmation does not match."""
        url = reverse("register")
        payload = {
            "username": "invalid_customer",
            "email": "invalid_customer@example.com",
            "password": "securepass123",
            "repeated_password": "differentpass123",
            "type": "customer",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username="invalid_customer").count(), 0)

    def test_login_returns_existing_token_and_user_data(self):
        """Ensure login returns token and user data for valid credentials."""
        url = reverse("login")
        user = User.objects.create_user(
            username="existing_user",
            email="existing_user@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=user, type="business")

        response = self.client.post(
            url,
            {"username": "existing_user", "password": "securepass123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], user.username)
        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(response.data["user_id"], user.id)

    def test_login_rejects_invalid_credentials(self):
        """Ensure login rejects an invalid username and password combination."""
        url = reverse("login")
        user = User.objects.create_user(
            username="existing_user",
            email="existing_user@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=user, type="customer")

        response = self.client.post(
            url,
            {"username": "existing_user", "password": "wrongpass123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
