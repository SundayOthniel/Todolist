from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    address = models.CharField(max_length=253)
    email = models.EmailField(max_length=254, unique=True)
    gender = models.CharField(max_length=6)
    phone = models.CharField(max_length=15)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =[]