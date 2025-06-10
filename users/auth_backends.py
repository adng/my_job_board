from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None):
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            return None
