from rest_framework import serializers
from accounts.models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['mobile', 'password','email', 'first_name', 'last_name']


class VerifyOtpSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=4, write_only=True)



class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)
    password = serializers.CharField(write_only=True)


class LogOutSerializer(serializers.Serializer):
    pass