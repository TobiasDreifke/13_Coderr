from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail
from reviews_app.models import Review
from user_auth_app.models import UserProfile


class BaseInfoTests(APITestCase):
    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=self.business_user, type="business")

        self.customer_user = User.objects.create_user(
            username="customer_user",
            email="customer@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=self.customer_user, type="customer")

        offer = Offer.objects.create(
            user=self.business_user,
            title="Website Design",
            description="Professional design package",
        )
        for offer_type, price in (
            ("basic", 100),
            ("standard", 200),
            ("premium", 300),
        ):
            OfferDetail.objects.create(
                offer=offer,
                title=f"{offer_type.title()} Package",
                revisions=2,
                delivery_time_in_days=5,
                price=price,
                features=["feature"],
                offer_type=offer_type,
            )

        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description="Very good",
        )

        second_customer = User.objects.create_user(
            username="second_customer",
            email="second_customer@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=second_customer, type="customer")
        Review.objects.create(
            business_user=self.business_user,
            reviewer=second_customer,
            rating=5,
            description="Excellent",
        )

    def test_base_info_returns_aggregated_platform_stats(self):
        url = reverse("base-info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["review_count"], 2)
        self.assertEqual(response.data["average_rating"], 4.5)
        self.assertEqual(response.data["business_profile_count"], 1)
        self.assertEqual(response.data["offer_count"], 1)
