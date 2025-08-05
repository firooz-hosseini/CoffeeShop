from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Notification
from products.models import Product
from .forms import CreateOrderItemForm

class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = CreateOrderItemForm()
        return render(request, 'order/create_order.html', {'product': product, 'form': form})

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = CreateOrderItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            order = Order.objects.create(user=request.user)
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            Notification.objects.create(
            message=f'New order by {request.user.mobile} for {quantity} x {product.title}')
            return redirect('order_success')
        return render(request, 'order/create_order.html', {'product': product, 'form': form})


def order_success(request):
    return render(request, 'order/order_success.html')