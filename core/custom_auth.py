

from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class CustomAuthBackend(BaseBackend):
    def __init__(self):
        pass
    def authenticate(self, username=None, password=None, *args, **kwargs):
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None

        # Check the password
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
