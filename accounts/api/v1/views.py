from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import LoginSerializer, SignUpSerializer, VerifyOtpSerializer, ProfileSerializer, FavoriteSerializer, OrderSerializer, OrderItemSerializer
from accounts.models import CustomUser
from products.models import Favorite
from orders.models import Order
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.core.cache import cache
from .sms_utils import send_sms
import random

from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny



class SignUpApiViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer

    def create(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data["mobile"]
            password = serializer.validated_data["password"]
            password = serializer.validated_data["password"]
            email = serializer.validated_data.get("email")
            first_name = serializer.validated_data.get("first_name")
            last_name = serializer.validated_data.get("last_name")

            otp_code = str(random.randint(1000, 9999))
            cache.set(f"otp_{otp_code}", {
                "mobile": mobile,
                "password": password,
                "email": email,
                "first_name": first_name,
                "last_name": last_name
            }, timeout=300)
            send_sms(mobile, f"Your OTP code: {otp_code}", test=True)
            return Response({"message": "OTP sent (test mode)"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyOtpApiViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = VerifyOtpSerializer

    def create(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data["otp_code"]
            cached_data = cache.get(f"otp_{otp_code}")
            if not cached_data:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


            mobile = cached_data["mobile"]
            password = cached_data["password"]
            email = cached_data.get("email")
            first_name = cached_data.get("first_name")
            last_name = cached_data.get("last_name")

            user, created = CustomUser.objects.get_or_create(
                mobile=mobile,
                defaults={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name
                }
            )
            
            if created:
                user.set_password(password)
                user.save()

            cache.delete(f"otp_{otp_code}")

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User created successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer


    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data["mobile"]
            password = serializer.validated_data["password"]
            
            user = authenticate(request, mobile=mobile, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid mobile or password"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out from this device."}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class FullProfileViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    
    def list(self, request):
        user = request.user

        profile_data = ProfileSerializer(user).data
        favorites = Favorite.objects.filter(user=user)
        favorites_data = FavoriteSerializer(favorites, many=True).data
        orders = Order.objects.filter(user=user)
        orders_data = OrderSerializer(orders, many=True).data
        orders_items_data = {}
        for order in orders:
            orders_items_data[order.id] = OrderItemSerializer(order.items.all(), many=True).data

        return Response({
            "profile": profile_data,
            "favorites": favorites_data,
            "orders": orders_data,
            "order_items": orders_items_data,

        })
    

class ProfileViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoriteViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def list_favorite(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete_favorite(self, request, pk=None):
        try:
            fav = Favorite.objects.get(pk=pk, user=request.user)
            fav.delete()
            return Response({"detail": "Favorite deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)



class OrderViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def list_order(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='items')
    def items_order(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
            serializer = OrderItemSerializer(order.items.all(), many=True)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=404)

