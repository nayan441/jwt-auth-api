from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
class CustomUser(AbstractUser):
    pass


class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.title}  -  {self.user.id}"

class OutstandingRefreshToken(models.Model):
    jti =models.UUIDField(unique=True, max_length=255, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    token = models.TextField(unique=True)
    expire_at =  models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class BlacklistedRefreshToken(models.Model):
    token = models.ForeignKey(OutstandingRefreshToken, on_delete=models.DO_NOTHING)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

