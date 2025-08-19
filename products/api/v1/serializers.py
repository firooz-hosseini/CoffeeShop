from rest_framework import serializers
from products.models import Product, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        field = ['id', 'image', 'is_main']


class ProductSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField(many=True)
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['__all__']
        ingredient= serializers.StringRelatedField(many=True)

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        for image_data in images_data:
            Image.objects.create(product=product, **image_data)
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        if images_data is not None:
            instance.images.all().delete()
            for image_data in images_data:
                Image.objects.create(product=instance, **image_data)

        return instance