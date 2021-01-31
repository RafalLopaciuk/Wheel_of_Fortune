import uuid
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Server(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False)
    create_date = models.DateTimeField(auto_now=True)
    activate = models.BooleanField(default=True, null=False)
    link_string = models.CharField(max_length=100, null=False, default="")
    max_players = models.IntegerField(default=3, null=False)
    count_players = models.IntegerField(default=0, null=False)
    user_create = models.ForeignKey(User, on_delete=models.CASCADE)


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
    active_game = models.OneToOneField(
        Server,
        on_delete=models.SET_NULL,
        default=None,
        null=True
    )
