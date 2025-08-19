from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random


class CustomUserManger(BaseUserManager):

    def create_user(self,mobile,password,**extra_field):
        user = self.model(mobile=mobile, **extra_field)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,mobile , password,  **extra_fields):
        extra_fields.setdefault("is_staff", True) 
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(mobile, password, **extra_fields) 

class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=11,unique=True)
    profile_picture = models.ImageField(upload_to='user_picture/',null=True,blank=True)
    username = None
    USERNAME_FIELD = 'mobile'
    objects = CustomUserManger()

    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    
    def generate_otp(self):
        self.otp_code = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp_code

    def otp_valid(self):
        return self.otp_created_at and self.otp_created_at + timezone.timedelta(minutes=5) > timezone.now()

    def __str__(self):
        return self.mobile