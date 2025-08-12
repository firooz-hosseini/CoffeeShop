from django.db import models

from accounts.models import CustomUser


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredient = models.ManyToManyField('Ingredient',related_name='product_ingredient')
    category = models.ForeignKey('Category',on_delete=models.CASCADE,related_name='product_category')
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    def is_available(self):
        return self.quantity > 0
    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='product_image/')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='image_product')

    def __str__(self):
        return self.product.title
    

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='favorite_user')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='favorite_product')

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user} - {self.product.title}'