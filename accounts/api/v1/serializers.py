from rest_framework import serializers
from accounts.models import CustomUser

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['mobile', 'password']

    def validate_mobile(self, value):
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("Mobile number must be 11 digits")
        return value

class VerifyOtpSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)
    otp_code = serializers.CharField(max_length=4, write_only=True)

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        otp= attrs.get('otp_code')

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
