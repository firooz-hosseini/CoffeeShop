from django.contrib import admin
from .models import *
from django.contrib import admin
from .models import Order, OrderItem, Rating, Comment

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ('time', 'items__product__category')  
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
admin.site.register(Rating)
admin.site.register(Comment)

