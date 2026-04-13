from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from orders_app.models import Order
from user_auth_app.models import UserProfile


class OrderPermissionTests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer_user",
            email="customer@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=self.customer, type="customer")

        self.business_owner = User.objects.create_user(
            username="business_owner",
            email="owner@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=self.business_owner, type="business")

        self.other_business = User.objects.create_user(
            username="other_business",
            email="other_business@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=self.other_business, type="business")

        self.order = Order.objects.create(
            customer_user=self.customer,
            business_user=self.business_owner,
            title="Logo Design",
            revisions=2,
            delivery_time_in_days=4,
            price=100,
            features=["Logo"],
            offer_type="basic",
            status="in_progress",
        )

    def test_only_assigned_business_user_can_patch_order(self):
        token = Token.objects.create(user=self.other_business)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {"status": "completed"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assigned_business_user_can_patch_order(self):
        token = Token.objects.create(user=self.business_owner)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {"status": "completed"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")
