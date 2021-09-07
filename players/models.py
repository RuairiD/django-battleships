from django.contrib.auth.models import User
from django.db import models


class Player(models.Model):
    user = models.OneToOneField(User,
            on_delete=models.CASCADE)

    def __str__(self):
        return '{username}'.format(
            username=self.user.username
        )
