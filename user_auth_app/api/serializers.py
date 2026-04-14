from rest_framework import serializers
from ..models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """Serialize user profile registration data."""

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'repeated_password', 'type']


class RegistrationSerializer(serializers.ModelSerializer):
    """Validate and create a new authenticated user account."""

    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(
        choices=UserProfile.TYPE_CHOICES, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate_email(self, value):
        """Reject duplicate email addresses during registration."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate(self, data):
        """Ensure both submitted passwords match."""
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def validate_username(self, value):
        """Reject duplicate usernames during registration."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value

    def save(self):
        """Create the user, hash the password, and create the linked profile."""
        pw = self.validated_data['password']
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        user.set_password(pw)
        user.save()
        UserProfile.objects.create(
            username=user,
            type=self.validated_data.get('type')
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Validate user credentials for token-based login."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Authenticate a user by username and password."""
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid username or password")

        data['user'] = user
        return data
