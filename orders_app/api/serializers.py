from rest_framework import serializers
from ..models import Order
from offers_app.models import OfferDetail


class OrderSerializer(serializers.ModelSerializer):
    """Serialize order instances for read-only API responses."""

    class Meta:
        model = Order
        fields = [
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id', 'customer_user', 'business_user',
            'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type',
            'status', 'created_at', 'updated_at'
        ]


class OrderUpdateSerializer(serializers.ModelSerializer):
    """Serialize order instances for business-side status updates."""

    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user',
                  'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type',
                  'status', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.Serializer):
    """Validate input and create an order from an existing offer detail."""

    offer_detail_id = serializers.IntegerField()

    def validate_offer_detail_id(self, value):
        """Ensure the referenced offer detail exists before creating an order."""
        try:
            OfferDetail.objects.get(id=value)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError("Offer detail not found.")
        return value

    def create(self, validated_data):
        """Copy the selected offer detail data into a new order instance."""
        offer_detail_id = validated_data['offer_detail_id']

        offer_detail = OfferDetail.objects.select_related('offer__user').get(
            id=offer_detail_id
        )

        order = Order.objects.create(
            customer_user=self.context['request'].user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )

        return order
