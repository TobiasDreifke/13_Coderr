from rest_framework import serializers

from ..models import Offer, OfferDetail


class BaseOfferSerializer(serializers.ModelSerializer):
    """Provide shared computed fields for offer serializers."""

    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    def get_min_price(self, obj):
        """Return the lowest price across the offer's detail variants."""
        prices = obj.details.values_list('price', flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        """Return the shortest delivery time across the offer's detail variants."""
        delivery_times = obj.details.values_list(
            'delivery_time_in_days', flat=True
        )
        return min(delivery_times) if delivery_times else None


class OfferDetailSerializer(serializers.ModelSerializer):
    """Serialize a single offer detail variant."""

    offer_type = serializers.ChoiceField(
        choices=['basic', 'standard', 'premium'],
        error_messages={
            'invalid_choice': 'Invalid type. Allowed values are: basic, standard, premium.'
        },
    )

    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
        ]
        read_only_fields = ['id']


class OfferSerializer(BaseOfferSerializer):
    """Serialize full offers including their three required detail variants."""

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_details(self, value):
        """Require exactly one basic, standard, and premium offer detail."""
        if len(value) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly 3 details."
            )
        types = {detail['offer_type'] for detail in value}
        required = {'basic', 'standard', 'premium'}
        if types != required:
            raise serializers.ValidationError(
                f"Details must contain {required}, not {types}."
            )
        return value

    def create(self, validated_data):
        """Create an offer and its nested detail records for the current user."""
        details_data = validated_data.pop('details')
        validated_data['user'] = self.context['request'].user
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer


class OfferUpdateSerializer(OfferSerializer):
    """Serialize partial updates for offers and their nested details."""

    details = OfferDetailSerializer(many=True, required=False)

    def validate_details(self, value):
        """Require each submitted detail update to declare its offer type."""
        for detail in value:
            if 'offer_type' not in detail:
                raise serializers.ValidationError(
                    "Each detail must include an offer_type."
                )
        return value

    def update(self, instance, validated_data):
        """Update offer fields and matching nested detail records by type."""
        details_data = validated_data.pop('details', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for detail_data in details_data:
            offer_type = detail_data.get('offer_type')
            try:
                detail = instance.details.get(offer_type=offer_type)
            except OfferDetail.DoesNotExist:
                raise serializers.ValidationError(
                    {"details": f"No detail with offer_type '{offer_type}' was found."}
                )
            for attr, value in detail_data.items():
                setattr(detail, attr, value)
            detail.save()

        return instance


class OfferDetailNestedSerializer(serializers.ModelSerializer):
    """Serialize linked detail resources by identifier and URL."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        """Return the API URL for the nested offer detail resource."""
        return f'/api/offerdetails/{obj.id}/'


class OfferListSerializer(BaseOfferSerializer):
    """Serialize offers for listing endpoints with user summary data."""

    details = OfferDetailNestedSerializer(many=True, read_only=True)
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details',
        ]

    def get_user_details(self, obj):
        """Return public name fields for the offer owner."""
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'username': obj.user.username,
        }


class OfferRetrieveSerializer(OfferListSerializer):
    """Serialize a single offer without the list-only user summary field."""

    class Meta(OfferListSerializer.Meta):
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
        ]
