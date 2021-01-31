import uuid

from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        default=None,
    )
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    amount_of_money = models.FloatField(default=0.0)
