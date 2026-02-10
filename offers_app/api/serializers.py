from rest_framework import serializers
from ..models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type'
        ]
        read_only_fields = ['id']


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

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
            'min_delivery_time'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_min_price(self, obj):
        prices = obj.details.values_list('price', flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        delivery_times = obj.details.values_list(
            'delivery_time_in_days', flat=True)
        return min(delivery_times) if delivery_times else None

  

    def validate_details(self, value):

        if len(value) != 3:
            raise serializers.ValidationError(
                "Ein Offer muss genau 3 Details haben"
            )

        types = {detail['offer_type'] for detail in value} 
        required = {'basic', 'standard', 'premium'}

        if types != required:
            raise serializers.ValidationError(
                f"Details müssen {required} enthalten, nicht {types}"
            )

        return value
