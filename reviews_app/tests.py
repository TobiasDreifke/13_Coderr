from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from reviews_app.models import Review
from user_auth_app.models import UserProfile


class ReviewFilterTests(APITestCase):
    """Verify review list filtering behavior."""

    def setUp(self):
        """Create users, reviews, and authentication for filter tests."""
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
        """Ensure the review list can be filtered by business user ID."""
        url = reverse("review-list-create")
        response = self.client.get(
            url,
            {"business_user_id": self.business_one.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.review_one.id)

    def test_review_list_filters_by_reviewer_id(self):
        """Ensure the review list can be filtered by reviewer ID."""
        url = reverse("review-list-create")
        response = self.client.get(
            url,
            {"reviewer_id": self.customer.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["reviewer"], self.customer.id)


class ReviewEndpointTests(APITestCase):
    """Verify review endpoint permissions and ownership behavior."""

    def setUp(self):
        """Create users and an existing review for endpoint tests."""
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

        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@example.com",
            password="securepass123",
        )
        UserProfile.objects.create(username=self.business_user, type="business")

        self.review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer,
            rating=4,
            description="Very good",
        )

    def authenticate(self, user):
        """Authenticate the test client as the given user."""
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_review_list_requires_authentication(self):
        """Ensure the review list endpoint requires authentication."""
        url = reverse("review-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_create_requires_customer_user(self):
        """Ensure only customer users can create reviews."""
        self.authenticate(self.business_user)
        url = reverse("review-list-create")

        response = self.client.post(
            url,
            {"business_user": self.business_user.id, "rating": 5, "description": "Great"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_create_saves_authenticated_user_as_reviewer(self):
        """Ensure the authenticated customer is saved as the reviewer."""
        self.authenticate(self.other_customer)
        url = reverse("review-list-create")

        response = self.client.post(
            url,
            {
                "business_user": self.business_user.id,
                "rating": 5,
                "description": "Excellent work",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["reviewer"], self.other_customer.id)

    def test_review_create_rejects_duplicate_review_for_same_business_user(self):
        """Ensure duplicate reviews for the same business user are rejected."""
        self.authenticate(self.customer)
        url = reverse("review-list-create")

        response = self.client.post(
            url,
            {
                "business_user": self.business_user.id,
                "rating": 5,
                "description": "Duplicate review",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_patch_allows_owner(self):
        """Ensure review owners can update their reviews."""
        self.authenticate(self.customer)
        url = reverse("review-update-destroy", kwargs={"pk": self.review.id})

        response = self.client.patch(
            url,
            {"rating": 5, "description": "Even better"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 5)

    def test_review_patch_forbids_non_owner(self):
        """Ensure non-owners cannot update a review."""
        self.authenticate(self.other_customer)
        url = reverse("review-update-destroy", kwargs={"pk": self.review.id})

        response = self.client.patch(
            url,
            {"rating": 2},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_delete_allows_owner(self):
        """Ensure review owners can delete their reviews."""
        self.authenticate(self.customer)
        url = reverse("review-update-destroy", kwargs={"pk": self.review.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())
