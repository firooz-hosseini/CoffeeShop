from django.db import models
from accounts.models import CustomUser

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredient = models.ManyToManyField('Ingredient',related_name='product_ingredient')
    category = models.ForeignKey('Category',on_delete=models.CASCADE,related_name='product_category')
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()


class Ingredient(models.Model):
    title = models.CharField(max_length=50)


class Category(models.Model):
    title = models.CharField(max_length=50)


class Image(models.Model):
    image = models.ImageField(upload_to='product_image/')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='image_product')
    

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='favorite_user')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='favorite_product')



