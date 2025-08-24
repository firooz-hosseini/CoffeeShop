from rest_framework import serializers, permissions
from products.models import Product,Category,Image, Favorite

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'is_main']


class ProductSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField(many=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source="category", write_only=True)
    image = ImageSerializer(many=True, required=False, source='image_product')
    is_available = serializers.BooleanField(read_only=True)
    permission_classes = [permissions.IsAuthenticated]

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        image_data = validated_data.pop('image_product', [])
        product = Product.objects.create(**validated_data)
        main_found = False
        for img in image_data:
            if img.get('is_main', False):
                if main_found:
                    img['is_main'] = False
                else:
                    main_found = True
            Image.objects.create(product=product, **img)
        return product


    def update(self, instance, validated_data):
        image_data = validated_data.pop('image_product', None)

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        if image_data is not None:
            instance.image.all().delete()
            main_found = False
            for img in image_data:
                if img.get('is_main', False):
                    if main_found:
                        img['is_main'] = False
                    else:
                        main_found = True
                Image.objects.create(product=instance, **img)

        return instance
    

class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'product']