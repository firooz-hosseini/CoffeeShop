from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem
from products.models import Product

class CreateOrderView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        order = Order.objects.create(user=request.user)
        OrderItem.objects.create(order=order, product=product, quantity=1)
        return redirect('order_success')
