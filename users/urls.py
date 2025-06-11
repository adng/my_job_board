"""
User endpoints.
"""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import (
    SignUpView,
    EmailTokenObtainPairView,
    EmailTokenRefreshView,
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="sign_up"),  # Register
    path(
        "token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # JWT login
    path(
        "token/refresh/", EmailTokenRefreshView.as_view(), name="token_refresh"
    ),  # JWT refresh
]
