from rest_framework import serializers

from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serialize review records and enforce one review per business user."""

    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate(self, data):
        """Prevent duplicate reviews from the same user to the same business user."""
        request = self.context.get('request')
        business_user = data.get('business_user')

        if not self.instance:
            if Review.objects.filter(
                reviewer=request.user,
                business_user=business_user,
            ).exists():
                raise serializers.ValidationError(
                    "You have already submitted a review for this business user."
                )
        return data

    def create(self, validated_data):
        """Store the authenticated user as the review author."""
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Serialize review updates while keeping ownership fields read-only."""

    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'business_user', 'reviewer', 'created_at', 'updated_at']
