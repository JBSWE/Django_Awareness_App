from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    points = models.IntegerField(default=0)
