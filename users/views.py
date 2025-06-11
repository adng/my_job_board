from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import exceptions, generics, serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_api_key.permissions import HasAPIKey

from users.serializers import SignUpSerializer, EmailTokenObtainPairView


class SignUpView(generics.CreateAPIView):
    """
    Register a new user.
    """

    serializer_class = SignUpSerializer
    permission_classes = (AllowAny, HasAPIKey)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        User = get_user_model()
        user = User.objects.create_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        return Response(
            {"id": user.id, "email": user.email},
            status=status.HTTP_201_CREATED,
        )


class SignOutView(APIView):
    """
    Sign out by blacklisting the refresh token.
    """

    permission_classes = (HasAPIKey,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Signed out."}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {"detail": "Invalid token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT token serializer using email.
    """

    username_field = "email"


class EmailTokenObtainPairView(TokenObtainPairView):
    """
    Obtain JWT token with email/password.
    """

    serializer_class = EmailTokenObtainPairSerializer


class EmailTokenRefreshView(TokenRefreshView):
    """
    Refresh JWT token.
    """

    serializer_class = TokenRefreshSerializer
