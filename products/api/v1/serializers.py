from rest_framework import serializers
from products.models import Product,Category,Image, Favorite

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'is_main']


class ProductSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField(many=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source="category", write_only=True)
    image = ImageSerializer(many=True, required=False)
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        image_data = validated_data.pop('image', [])
        product = Product.objects.create(**validated_data)
        for image_data in image_data:
            Image.objects.create(product=product, **image_data)
        return product

    def update(self, instance, validated_data):
        image_data = validated_data.pop('image', None)

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        if image_data is not None:
            instance.image.all().delete()
            for image_data in image_data:
                Image.objects.create(product=instance, **image_data)

        return instance
    

class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Product
        field = ['id', 'product']
