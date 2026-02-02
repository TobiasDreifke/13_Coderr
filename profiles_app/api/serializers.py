from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    # Fields from User model
    user = serializers.IntegerField(source='id', read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    # Fields from UserProfile model
    file = serializers.ImageField(
        source='profile.file', required=False, allow_null=True)
    location = serializers.CharField(
        source='profile.location', required=False, allow_blank=True)
    tel = serializers.CharField(
        source='profile.tel', required=False, allow_blank=True)
    description = serializers.CharField(
        source='profile.description', required=False, allow_blank=True)
    working_hours = serializers.CharField(
        source='profile.working_hours', required=False, allow_blank=True)
    type = serializers.CharField(source='profile.type', read_only=True)
    created_at = serializers.DateTimeField(
        source='profile.created_at', read_only=True)

    class Meta:
        model = User
        fields = [
            "user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type", "email", "created_at"
        ]

    def update(self, instance, validated_data):
        # Update User fields
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update UserProfile fields
        profile_data = validated_data.get('profile', {})
        profile = instance.profile

        profile.file = profile_data.get('file', profile.file)
        profile.location = profile_data.get('location', profile.location)
        profile.tel = profile_data.get('tel', profile.tel)
        profile.description = profile_data.get(
            'description', profile.description)
        profile.working_hours = profile_data.get(
            'working_hours', profile.working_hours)
        profile.save()

        return instance


class BusinessProfileSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type']


class CustomerProfileSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'type']
