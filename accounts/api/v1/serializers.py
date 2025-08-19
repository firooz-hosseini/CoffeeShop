from rest_framework import serializers
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['mobile', 'password']

    def create(self, validated_data):
        temp_user = CustomUser(
            mobile=validated_data['mobile'],
            password=make_password(validated_data['password'])
        )
        temp_user.generate_otp()
        return temp_user

class VerifyOtpSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    otp_code = serializers.CharField(write_only=True)

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        otp = attrs.get('otp_code')

        try:
            user = CustomUser.objects.get(mobile=mobile)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("No signup request found for this mobile")

        if not user.otp_valid() or user.otp_code != otp:
            raise serializers.ValidationError("Invalid or expired OTP")

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        user.is_active = True
        user.otp_code = None
        user.otp_created_at = None
        user.save()
        return user
