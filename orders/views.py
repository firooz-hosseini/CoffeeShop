from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Order, OrderItem, Notification
from products.models import Product
from django.views.generic import ListView
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
            Notification.objects.create(message=f'New order by {request.user.mobile} for {quantity} x {product.title}')
            return redirect('order_success')
        return render(request, 'order/create_order.html', {'product': product, 'form': form})


def order_success(request):
    return render(request, 'order/order_success.html')


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product__image_product')

def cancel_order_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    try:
        order.mark_as_canceled()
        messages.success(request, 'The order was successfully canceled')
    except ValueError as e:
        messages.error(request, str(e))

    return redirect('order_list')