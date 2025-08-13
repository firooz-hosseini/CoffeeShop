from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from products.models import Product

from .forms import CreateOrderItemForm
from .models import Comment, Notification, Order, OrderItem


class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if product.quantity <= 0:
            messages.error(request,'This product is out of stock.')
            return redirect('product-detail',pk=product.pk)
        
        form = CreateOrderItemForm()
        return render(request, 'order/create_order.html', {'product': product, 'form': form})

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if product.quantity <= 0:
            messages.error(request, "This product is out of stock.")
            return redirect('product-detail', pk=product.pk)

        form = CreateOrderItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity > product.quantity:
                messages.error(request, f"Only {product.quantity} items are available.")
                return redirect('product-detail', pk=product.pk)

            order = Order.objects.create(user=request.user)
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

            product.quantity -= quantity
            product.save()
            
            Notification.objects.create(message=f'New order by {request.user.mobile} for {quantity} x {product.title}')
            messages.success(request, f'{quantity} {product.title} is added to your order.')

            return redirect('product-detail', pk=product.pk)
        return render(request, 'product_detail.html', {'product': product, 'form': form})


def order_success(request):
    return render(request, 'order/order_success.html')


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status='pending').prefetch_related('items__product__image_product')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = context['orders']
        context['total_all_orders'] = sum(order.total_price for order in orders)
        return context

@login_required
def cancel_order_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    try:
        order.mark_as_canceled()
        messages.success(request, 'The order was successfully canceled')
    except ValueError as e:
        messages.error(request, str(e))

    return redirect('order_list')

@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders':orders})
 
@login_required
def delete_order_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    if request.method == 'POST':
        order.delete()
        return redirect('order_list')


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