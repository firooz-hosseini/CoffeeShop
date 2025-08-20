from rest_framework import serializers
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password
from django.core.cache import cache


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['mobile', 'password']


class VerifyOtpSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=4, write_only=True)

