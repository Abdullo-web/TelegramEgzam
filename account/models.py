from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    phone_number = models.CharField(max_length=13,unique=True)


    def __str__(self):
        return self.phone_number
