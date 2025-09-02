from django.db import models

from accounts.models import CustomUser
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('paid', 'paid'),
        ('delivered', 'delivered'),
        ('canceled', 'canceled'),
    ]

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='order_user')
    time = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    seen_by_admin = models.BooleanField(default=False)

    
    @property
    def total_price(self):
        return sum((item.product.price * item.quantity for item in self.items.all()))
    
    def mark_as_delivered(self):
        if self.status != 'pending':
            raise ValueError('Only pending orders can be marked as delivered.')
        self.status = 'delivered'
        self.save()

    def mark_as_canceled(self):
        if self.status != 'pending':
            raise ValueError('Only pending orders can be marked as canceled.')
        self.status = 'canceled'
        self.save()

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
    rate = [(1, 'very bad'), (2, 'bad'), (3, 'normal'),(4, 'good'),(5, 'very good')]
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
        return f"Notification: {self.message[:50]}"
    


class FinalOrder(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='final_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='paid')

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    def __str__(self):
        return f"FinalOrder {self.id} - {self.user.mobile}"


class FinalOrderItem(models.Model):
    final_order = models.ForeignKey(FinalOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
