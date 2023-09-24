from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField()


class FriendShip(models.Model):
    followee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="followee", on_delete=models.CASCADE)
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="follower", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} follow {}".format(self.follower.username, self.followee.username)

    class Meta:
        ordering = ["-created_at"]
