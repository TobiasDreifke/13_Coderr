from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail
from user_auth_app.models import UserProfile


class OfferListPaginationTests(APITestCase):
    """Verify pagination behavior for the offer list endpoint."""

    def setUp(self):
        """Create enough offers to exercise pagination behavior."""
        business_user = User.objects.create_user(
            username="business_user",
            email="business@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=business_user, type="business")

        for index in range(11):
            offer = Offer.objects.create(
                user=business_user,
                title=f"Offer {index}",
                description="Offer description",
            )
            for offer_type, price in (
                ("basic", 10),
                ("standard", 20),
                ("premium", 30),
            ):
                OfferDetail.objects.create(
                    offer=offer,
                    title=f"{offer_type} {index}",
                    revisions=1,
                    delivery_time_in_days=3,
                    price=price,
                    features=["feature"],
                    offer_type=offer_type,
                )

    def test_offer_list_uses_documented_page_query_parameter(self):
        """Ensure the offer list uses the documented page query parameter."""
        url = reverse("offer-list-create")
        response = self.client.get(url, {"page": 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class OfferEndpointTests(APITestCase):
    """Verify create, retrieve, update, and delete offer endpoints."""

    def setUp(self):
        """Create users, an offer, and nested details for endpoint tests."""
        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=self.business_user, type="business")

        self.other_business = User.objects.create_user(
            username="other_business",
            email="other_business@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=self.other_business, type="business")

        self.customer_user = User.objects.create_user(
            username="customer_user",
            email="customer@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=self.customer_user, type="customer")

        self.offer = Offer.objects.create(
            user=self.business_user,
            title="Website Design",
            description="Professional design package",
        )
        self.basic_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Package",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=["Logo"],
            offer_type="basic",
        )
        OfferDetail.objects.create(
            offer=self.offer,
            title="Standard Package",
            revisions=4,
            delivery_time_in_days=7,
            price=200,
            features=["Logo", "Flyer"],
            offer_type="standard",
        )
        OfferDetail.objects.create(
            offer=self.offer,
            title="Premium Package",
            revisions=6,
            delivery_time_in_days=10,
            price=300,
            features=["Logo", "Flyer", "Brand Guide"],
            offer_type="premium",
        )

    def authenticate(self, user):
        """Authenticate the test client as the given user."""
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_offer_create_requires_business_user(self):
        """Ensure customers cannot create offers."""
        self.authenticate(self.customer_user)
        url = reverse("offer-list-create")

        response = self.client.post(
            url,
            {
                "title": "New Offer",
                "description": "Offer description",
                "details": [
                    {
                        "title": "Basic",
                        "revisions": 1,
                        "delivery_time_in_days": 3,
                        "price": 50,
                        "features": ["Feature"],
                        "offer_type": "basic",
                    },
                    {
                        "title": "Standard",
                        "revisions": 2,
                        "delivery_time_in_days": 5,
                        "price": 100,
                        "features": ["Feature"],
                        "offer_type": "standard",
                    },
                    {
                        "title": "Premium",
                        "revisions": 3,
                        "delivery_time_in_days": 7,
                        "price": 150,
                        "features": ["Feature"],
                        "offer_type": "premium",
                    },
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_create_returns_created_offer_with_three_details(self):
        """Ensure a business user can create an offer with three details."""
        self.authenticate(self.business_user)
        url = reverse("offer-list-create")

        response = self.client.post(
            url,
            {
                "title": "New Offer",
                "description": "Offer description",
                "details": [
                    {
                        "title": "Basic",
                        "revisions": 1,
                        "delivery_time_in_days": 3,
                        "price": 50,
                        "features": ["Feature"],
                        "offer_type": "basic",
                    },
                    {
                        "title": "Standard",
                        "revisions": 2,
                        "delivery_time_in_days": 5,
                        "price": 100,
                        "features": ["Feature"],
                        "offer_type": "standard",
                    },
                    {
                        "title": "Premium",
                        "revisions": 3,
                        "delivery_time_in_days": 7,
                        "price": 150,
                        "features": ["Feature"],
                        "offer_type": "premium",
                    },
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data["details"]), 3)
        self.assertEqual(response.data["min_price"], 50)

    def test_offer_detail_requires_authentication(self):
        """Ensure the offer detail endpoint requires authentication."""
        url = reverse("offer-detail", kwargs={"pk": self.offer.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_detail_returns_offer_for_authenticated_user(self):
        """Ensure authenticated users can retrieve an offer with all details."""
        self.authenticate(self.customer_user)
        url = reverse("offer-detail", kwargs={"pk": self.offer.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.offer.id)
        self.assertEqual(len(response.data["details"]), 3)

    def test_offer_patch_updates_only_owner_offer(self):
        """Ensure the owner can update an offer and one nested detail."""
        self.authenticate(self.business_user)
        url = reverse("offer-detail", kwargs={"pk": self.offer.id})

        response = self.client.patch(
            url,
            {
                "title": "Updated Website Design",
                "details": [
                    {
                        "offer_type": "basic",
                        "title": "Updated Basic Package",
                        "price": 120,
                        "revisions": 3,
                        "delivery_time_in_days": 6,
                        "features": ["Logo", "Flyer"],
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.offer.refresh_from_db()
        self.basic_detail.refresh_from_db()
        self.assertEqual(self.offer.title, "Updated Website Design")
        self.assertEqual(self.basic_detail.title, "Updated Basic Package")
        self.assertEqual(float(self.basic_detail.price), 120.0)

    def test_offer_patch_forbids_non_owner(self):
        """Ensure non-owners cannot update another user's offer."""
        self.authenticate(self.other_business)
        url = reverse("offer-detail", kwargs={"pk": self.offer.id})

        response = self.client.patch(
            url,
            {"title": "Should not update"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_delete_allows_owner(self):
        """Ensure the owner can delete an offer."""
        self.authenticate(self.business_user)
        url = reverse("offer-detail", kwargs={"pk": self.offer.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Offer.objects.filter(id=self.offer.id).exists())

    def test_offer_detail_endpoint_requires_authentication(self):
        """Ensure the nested offer detail endpoint requires authentication."""
        url = reverse("offerdetail-detail", kwargs={"pk": self.basic_detail.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_detail_endpoint_returns_full_detail(self):
        """Ensure the nested offer detail endpoint returns full detail data."""
        self.authenticate(self.customer_user)
        url = reverse("offerdetail-detail", kwargs={"pk": self.basic_detail.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.basic_detail.id)
        self.assertEqual(response.data["offer_type"], "basic")
