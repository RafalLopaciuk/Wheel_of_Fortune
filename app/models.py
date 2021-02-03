import string
import uuid
from datetime import datetime
import random

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Server(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False)
    create_date = models.DateTimeField(auto_now=True)
    started = models.BooleanField(default=False, null=False)
    ended = models.BooleanField(default=False, null=False)
    link_string = models.CharField(default="room:" + str(name), max_length=100, null=False)
    max_players = models.IntegerField(default=3, null=False)
    count_players = models.IntegerField(default=0, null=False)
    user_create = models.ForeignKey(User, on_delete=models.CASCADE)
    max_rounds = models.IntegerField(default=3, null=False)
    actual_round = models.IntegerField(default=0, null=False)
    actual_word = models.CharField(max_length=100, default="123", null=False)
    actual_word_progres = models.CharField(max_length=100, default="___")
    actual_player_number = models.IntegerField(default=0, null=False)
    start_send_count = models.IntegerField(default=0, null=False)
    actual_word_hint = models.CharField(max_length=100, default="")


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
    active_game = models.ForeignKey(
        Server,
        on_delete=models.SET_NULL,
        default=None,
        null=True
    )
    actual_coins = models.IntegerField(default=0)
    actual_winning_coins = models.IntegerField(default=0)
