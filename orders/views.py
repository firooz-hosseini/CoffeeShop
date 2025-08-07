from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView
from .models import Order, OrderItem, Product, Comment
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


def deliver_order_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if not request.user.is_staff:
        messages.error(request, 'You do not have permission!')
        return redirect ('order_list')
    
    try:
        order.mark_as_delivered()
        messages.success(request, 'The order was successfully delivered')
    except ValueError as e:
        messages.error(request, str(e))

    return redirect('order_list')


def cancel_order_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    try:
        order.mark_as_canceled()
        messages.success(request, 'The order was successfully canceled')
    except ValueError as e:
        messages.error(request, str(e))

    return redirect('order_list')


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders':orders})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']
    template_name = 'order/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=kwargs['product_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = self.product
        if not form.instance.purchased_before:
            return self.handle_no_permission()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.product.pk})