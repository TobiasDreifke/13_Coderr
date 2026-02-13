from rest_framework import serializers
from ..models import Offer, OfferDetail


class BaseOfferSerializer(serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    def get_min_price(self, obj):
        prices = obj.details.values_list('price', flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        delivery_times = obj.details.values_list(
            'delivery_time_in_days', flat=True)
        return min(delivery_times) if delivery_times else None


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


class OfferSerializer(BaseOfferSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

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

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        validated_data['user'] = self.context['request'].user
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])
        
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
       
        for detail_data in details_data:
            offer_type = detail_data.get('offer_type')
            detail = instance.details.get(offer_type=offer_type)
            
            for attr, value in detail_data.items():
                setattr(detail, attr, value)
            detail.save()
        
        return instance


class OfferDetailNestedSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f'/api/offerdetails/{obj.id}/'


class OfferListSerializer(BaseOfferSerializer):
    details = OfferDetailNestedSerializer(many=True, read_only=True)
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time', 'user_details'
        ]

    def get_user_details(self, obj):
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'username': obj.user.username,
        }


class OfferRetrieveSerializer(OfferListSerializer):
    class Meta(OfferListSerializer.Meta):
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time'
        ]
