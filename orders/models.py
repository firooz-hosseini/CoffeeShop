from django.db import models
from products.models import Product
from accounts.models import CustomUser


class Order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='order_user')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_product')
    time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='Comment_user')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='Comment_product')
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)




class Rating(models.Model):
    rate = [(1, 'very bad'), (2, "bad"), (3, "normal"),(4, "good"),(5, "very good")]
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='Rating_user')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='Rating_product')
    score = models.CharField(choices=rate)
