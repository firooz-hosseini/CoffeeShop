from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class CustomUser(AbstractUser):

    phone = models.CharField(max_length=11,unique=True)
    profile_picture = models.ImageField(upload_to='user_picture/',null=True,blank=True)

              
