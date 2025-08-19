from rest_framework import serializers
from products.models import Product,Ingredient


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        ingredient= serializers.StringRelatedField(many=True)
