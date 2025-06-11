from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class SignUpSerializer(serializers.Serializer):
    """
    Serializer for user registration.
    """

    email = serializers.EmailField(write_only=True)  # User email
    password = serializers.CharField(write_only=True)  # User password

    def validate_email(self, value):
        User = get_user_model()

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User already exists")

        return value


class EmailTokenObtainPairView(TokenObtainPairSerializer):
    username_field = "email"
