from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from reviews_app.models import Review
from user_auth_app.models import UserProfile


class ReviewFilterTests(APITestCase):
    def setUp(self):
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

        self.business_one = User.objects.create_user(
            username="business_one",
            email="business1@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=self.business_one, type="business")

        self.business_two = User.objects.create_user(
            username="business_two",
            email="business2@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=self.business_two, type="business")

        self.token = Token.objects.create(user=self.customer)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.review_one = Review.objects.create(
            business_user=self.business_one,
            reviewer=self.customer,
            rating=5,
            description="Excellent",
        )
        Review.objects.create(
            business_user=self.business_two,
            reviewer=self.other_customer,
            rating=3,
            description="Okay",
        )

    def test_review_list_filters_by_business_user_id(self):
        response = self.client.get(
            "/api/reviews/",
            {"business_user_id": self.business_one.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.review_one.id)

    def test_review_list_filters_by_reviewer_id(self):
        response = self.client.get(
            "/api/reviews/",
            {"reviewer_id": self.customer.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["reviewer"], self.customer.id)
