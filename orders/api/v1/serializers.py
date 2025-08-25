from rest_framework import serializers
from orders.models import Order, OrderItem, Comment, Rating, Notification
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source="product.title")
    product_price = serializers.ReadOnlyField(source="product.price")

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'product_price', 'quantity']

