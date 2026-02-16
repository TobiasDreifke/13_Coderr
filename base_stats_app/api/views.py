from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Avg
from reviews_app.models import Review
from offers_app.models import Offer
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseInfoView(APIView):
    permission_classes = []  # Keine Permissions required!

    def get(self, request):
        review_count = Review.objects.count()

        average_rating = Review.objects.aggregate(
            avg=Avg('rating')
        )['avg']
        average_rating = round(average_rating, 1) if average_rating else 0.0

        business_profile_count = User.objects.filter(
            profile__type='business'
        ).count()

        offer_count = Offer.objects.count()

        return Response({
            'review_count': review_count,
            'average_rating': average_rating,
            'business_profile_count': business_profile_count,
            'offer_count': offer_count,
        })
