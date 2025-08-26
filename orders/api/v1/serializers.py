from rest_framework import serializers
from orders.models import Order, OrderItem, Comment, Rating, Notification
from products.models import Product,Image

class OrderItemInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image", "is_main"]

class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source="product.title")
    product_price = serializers.ReadOnlyField(source="product.price")
    product_image = ImageSerializer(source="product.image_product",many=True,read_only=True)
    product_quantity = serializers.ReadOnlyField(source="product.quantity",read_only=True)
    product_category = serializers.CharField(source="product.category.title",read_only=True)


    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'product_price', 'quantity','product_image','product_category', 'product_quantity']




class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only=True)
    total_price = serializers.ReadOnlyField()
    create_items = OrderItemInputSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'time', 'items', 'total_price','create_items']
        read_only_fields = ['user', 'status', 'time']
    def create(self, validated_data):
        items_data = validated_data.pop('create_items')
        order = Order.objects.create(user=self.context['request'].user, **validated_data)
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            if quantity > product.quantity:
                raise serializers.ValidationError(f"{product.title} فقط {product.quantity} موجود است")

            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            product.quantity -= quantity
            product.save()
        return order

class CommentSerializer(serializers.ModelSerializer):
    purchased_before = serializers.ReadOnlyField()
    is_approved = serializers.SerializerMethodField()
    verified_buyer = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'product', 'text', 'time','is_approved', 'purchased_before', 'verified_buyer']
        read_only_fields = ['user', 'time', 'is_approved', 'purchased_before', 'verified_buyer']
    
    def get_is_approved(self, obj):
        return obj.is_approved


    def get_verified_buyer(self, obj):
        return "Buyer approved"if obj.purchased_before else "buyer dont approved"
    

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id','user','product','score']
        read_only_fields = ['user']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']
        read_only_fields = ['message', 'created_at']