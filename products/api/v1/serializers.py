from rest_framework import serializers
from products.models import Product, Category, Image, Favorite, Ingredient
from orders.models import Comment, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'is_main']


class IngredientField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, obj):
        return obj.title

    def to_internal_value(self, data):
        if isinstance(data, int):
            return super().to_internal_value(data)
        ingredient = Ingredient.objects.filter(title=data).first()
        if not ingredient:
            ingredient = Ingredient.objects.create(title=data)
        return ingredient
    

class ProductSerializer(serializers.ModelSerializer):
    ingredient = IngredientField(queryset=Ingredient.objects.all(), many=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source="category", write_only=True)
    image = ImageSerializer(many=True, read_only=True, source='image_product') 
    is_available = serializers.BooleanField(read_only=True)
    

    class Meta:
        model = Product
        fields = '__all__'
    

class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'product']


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['id', 'product', 'text', 'is_approved']
        read_only = ['id', 'is_approved']

    def validate(self, data):
        user = self.context['request'].user
        product = data['product']

        if not OrderItem.objects.filter(order__user=user, product=product).exists():
            raise serializers.ValidationError('You can only leave comments for products you have purchased.')
        return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    

class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'time']


class ProductIngredientsSerializer(serializers.ModelSerializer):
    ingredients = serializers.StringRelatedField(many=True, source='ingredient')

    class Meta:
        model = Product
        fields = ['title', 'ingredients']