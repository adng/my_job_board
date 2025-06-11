from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import SignUpView, EmailTokenObtainPairView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="sign_up"),
    path(
        "token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
