from rest_framework import serializers
from products.models import Product,Ingredient,Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]


class ProductSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField(many=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source="category", write_only=True)
    class Meta:
        model = Product
        fields = '__all__'
