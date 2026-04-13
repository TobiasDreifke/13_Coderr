from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail
from user_auth_app.models import UserProfile


class OfferListPaginationTests(APITestCase):
    def setUp(self):
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
        response = self.client.get("/api/offers/", {"page": 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
