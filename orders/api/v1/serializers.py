from rest_framework import serializers
from orders.models import Order, OrderItem, Comment, Rating, Notification
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source="product.title")
    product_price = serializers.ReadOnlyField(source="product.price")
    product_image = serializers.ImageField(source="product.image",read_only=True)
    product_quantity = serializers.ReadOnlyField(source="product.quantity")
    product_category = serializers.CharField(source="product.category.title",read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'product_price', 'quantity','product_image','product_category', 'product_quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'time', 'items', 'total_price']
        read_only_fields = ['user', 'status', 'time']

class CommentSerializer(serializers.ModelSerializer):
    purchased_before = serializers.ReadOnlyField()
    is_approved = serializers.SerializerMethodField()
    verified_buyer = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'user', 'product', 'text', 'time','is_approved', 'purchased_before', 'verified_buyer']
        read_only_fields = ['user', 'time', 'is_approved', 'purchased_before', 'verified_buyer']

    def get_verified_buyer(self, obj):
        return "Buyer approved"if obj.purchased_before else "buyer dont approved"