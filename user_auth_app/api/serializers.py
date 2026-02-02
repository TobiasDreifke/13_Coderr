from rest_framework import serializers
from django.contrib.auth.models import User


# Example User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        

# Example Registration Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
#     
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user
