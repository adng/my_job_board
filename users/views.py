from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import exceptions, generics, serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import SignUpSerializer, EmailTokenObtainPairView


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny, HasAPIKey)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)

            User = get_user_model()
            User.objects.create_user(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )

            return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairView


# class LogInView(generics.GenericAPIView):
#     serializer_class = EmailSerializer
#     permission_classes = (AllowAny, HasAPIKey)

#     def post(self, request: Request, *args, **kwargs) -> Response:
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = self.authenticate(
#             request=request, validated_data=serializer.validated_data
#         )

#         return Response(status=status.HTTP_200_OK)

#     def authenticate(self, request, validated_data):
#         user = authenticate(request=request, **validated_data)

#         if user is None or not user.is_active:
#             raise exceptions.AuthenticationFailed(
#                 "Could not authenticate the user"
#             )

#         return user
