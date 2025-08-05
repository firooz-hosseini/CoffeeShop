from django.db import models
from products.models import Product
from accounts.models import CustomUser


class Order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='order_user')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} at {self.time} ordered'

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_item_product')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'Product: {self.product.title}, quantity: {self.quantity}'

class Comment(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='Comment_user')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='Comment_product')
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    @property
    def purchased_before(self):
        return OrderItem.objects.filter(order__user=self.user, product=self.product).exists()

    def __str__(self):
        return f'User: {self.user.first_name}, Product: {self.product.title}, Text: {self.text}'
    


class Rating(models.Model):
    rate = [(1, 'very bad'), (2, "bad"), (3, "normal"),(4, "good"),(5, "very good")]
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='Rating_user')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='Rating_product')
    score = models.IntegerField(choices=rate)

    class Meta:
        unique_together = ('user','product')

    def __str__(self):
        return f'User: {self.user.first_name}, Product: {self.product.title}, Score: {self.score}'
    

    
class Notification(models.Model):
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message[:50]