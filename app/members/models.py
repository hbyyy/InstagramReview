from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    """
    사용자모델로 쓰입니다
    """
    name = models.CharField(max_length=20, null=True)
