from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from user_auth_app.models import UserProfile


class OrderPermissionTests(APITestCase):
    """Verify order update permissions for assigned business users."""

    def setUp(self):
        """Create users and a sample order for permission tests."""
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
        """Ensure unrelated business users cannot update the order status."""
        url = reverse("order-update-destroy", kwargs={"pk": self.order.id})
        token = Token.objects.create(user=self.other_business)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.patch(
            url,
            {"status": "completed"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assigned_business_user_can_patch_order(self):
        """Ensure the assigned business user can update the order status."""
        url = reverse("order-update-destroy", kwargs={"pk": self.order.id})
        token = Token.objects.create(user=self.business_owner)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.patch(
            url,
            {"status": "completed"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")


class OrderEndpointTests(APITestCase):
    """Verify order listing, creation, deletion, and count endpoints."""

    def setUp(self):
        """Create users, offer details, and orders used by endpoint tests."""
        self.customer = User.objects.create_user(
            username="customer_user",
            email="customer@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=self.customer, type="customer")

        self.other_customer = User.objects.create_user(
            username="other_customer",
            email="other_customer@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=self.other_customer, type="customer")

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

        self.offer = Offer.objects.create(
            user=self.business_owner,
            title="Logo Design",
            description="Offer description",
        )
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Logo",
            revisions=2,
            delivery_time_in_days=4,
            price=100,
            features=["Logo"],
            offer_type="basic",
        )

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
        self.completed_order = Order.objects.create(
            customer_user=self.other_customer,
            business_user=self.business_owner,
            title="Website Design",
            revisions=3,
            delivery_time_in_days=5,
            price=200,
            features=["Website"],
            offer_type="standard",
            status="completed",
        )

    def authenticate(self, user):
        """Authenticate the test client as the given user."""
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_order_list_returns_only_orders_related_to_authenticated_user(self):
        """Ensure users only see orders where they are directly involved."""
        self.authenticate(self.customer)
        url = reverse("order-list-create")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.order.id)

    def test_order_create_requires_customer_user(self):
        """Ensure only customer users can create orders."""
        self.authenticate(self.business_owner)
        url = reverse("order-list-create")

        response = self.client.post(
            url,
            {"offer_detail_id": self.offer_detail.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_create_copies_offer_detail_into_order(self):
        """Ensure order creation copies the selected offer detail fields."""
        self.authenticate(self.customer)
        url = reverse("order-list-create")

        response = self.client.post(
            url,
            {"offer_detail_id": self.offer_detail.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["customer_user"], self.customer.id)
        self.assertEqual(response.data["business_user"], self.business_owner.id)
        self.assertEqual(response.data["title"], self.offer_detail.title)
        self.assertEqual(response.data["status"], "in_progress")

    def test_order_delete_requires_admin_user(self):
        """Ensure non-admin users cannot delete orders."""
        self.authenticate(self.business_owner)
        url = reverse("order-update-destroy", kwargs={"pk": self.order.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_delete_allows_admin_user(self):
        """Ensure admin users can delete orders."""
        admin_user = User.objects.create_user(
            username="admin_user",
            email="admin@example.com",
            password="securepass123",
            is_staff=True,
        )
        UserProfile.objects.create(username=admin_user, type="business")
        self.authenticate(admin_user)
        url = reverse("order-update-destroy", kwargs={"pk": self.order.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_order_count_returns_in_progress_orders_for_business_user(self):
        """Ensure the in-progress count endpoint returns the expected value."""
        self.authenticate(self.customer)
        url = reverse("order-count", kwargs={"business_user_id": self.business_owner.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order_count"], 1)

    def test_completed_order_count_returns_completed_orders_for_business_user(self):
        """Ensure the completed count endpoint returns the expected value."""
        self.authenticate(self.customer)
        url = reverse(
            "completed-order-count",
            kwargs={"business_user_id": self.business_owner.id},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed_order_count"], 1)
