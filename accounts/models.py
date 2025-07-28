from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

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
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManger()