from rest_framework import serializers
from accounts.models import CustomUser
from products.models import Favorite
from orders.models import Order, OrderItem


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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['mobile', 'email', 'first_name', 'last_name', 'profile_picture']


class FavoriteSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    class Meta:
        model = Favorite
        fields = ['id', 'product', 'product_title']


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    status = serializers.CharField()
    class Meta:
        model = Order
        fields = ['id', 'status', 'total_price', 'time']



class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'quantity']
