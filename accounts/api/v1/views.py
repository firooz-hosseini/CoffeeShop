from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import SignUpSerializer, VerifyOtpSerializer
from accounts.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache
from .sms_utils import send_sms
import random

class SignUpApiViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data["mobile"]
            otp_code = str(random.randint(1000, 9999))
            cache.set(f"otp_{mobile}", otp_code, timeout=300)
            send_sms(mobile, f"Your OTP code: {otp_code}", test=True)
            return Response({"message": "OTP sent (test mode)"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data["mobile"]
            otp_code = serializer.validated_data["otp_code"]

            cached_code = cache.get(f"otp_{mobile}")
            if cached_code != otp_code:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            user, created = CustomUser.objects.get_or_create(mobile=mobile)

            cache.delete(f"otp_{mobile}")

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User created successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)