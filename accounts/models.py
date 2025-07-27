from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11,unique=True)
    profile_picture = models.ImageField(upload_to='user_picture/',null=True,blank=True)
    username = None