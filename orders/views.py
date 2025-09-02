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
from .models import Comment, Notification, Order, OrderItem, Rating, FinalOrder


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
            
            Notification.objects.create(message=f'New order by {request.user.mobile} for {quantity} x {product.title}')
            messages.success(request, f'{quantity} {product.title} is added to your order.')

            return redirect('product-detail', pk=product.pk)
        return render(request, 'product_detail.html', {'product': product, 'form': form})


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
    

@login_required
def mark_as_paid(order):
        if order.status != 'pending':
            raise ValueError('Only pending orders can be marked as paid.')
        order.status = 'paid'
        order.save()


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']
    template_name = 'products/product_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=kwargs['product_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = self.product
        messages.success(self.request, "Your comment has been sent successfully. It will be shown after admin confirmation")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.product.pk})

@login_required
def pay_order_views(request):
    orders = Order.objects.filter(user=request.user, status='pending').prefetch_related('items__product')

    if not orders.exists():
        messages.error(request, 'There is no order to pay!')
        return redirect('order_list')
      
    if request.method == 'POST':
        try:
            for order in orders:
                for item in order.items.all():
                    product = item.product
                    if item.quantity > product.quantity:
                        messages.error(request, f"Not enough stock for {product.title}.")
                        return redirect('order_list')
                    product.quantity -= item.quantity
                    product.save()

                mark_as_paid(order)

            
            final_order = FinalOrder.objects.create(user=request.user, status='paid')
            final_order.orders.set(orders) 

            Notification.objects.create(
            message=f'New order by {request.user.first_name}, Order ID: {final_order.id}'
            )

        except ValueError as e:
            messages.error(request, str(e))
            return redirect('order_list')

        messages.success(request, 'The payment was successfully made!')
        return redirect('order_list')

    total_price_all = sum(order.total_price for order in orders)
    return render(request, 'order/payment.html', {
        'orders': orders,
        'total_price_all': total_price_all
    })


class RateProductView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        score = request.POST.get('score')

        try:
            score = int(score)
        except (TypeError, ValueError):
            messages.error(request, "Invalid score.")
            return redirect('product-detail', pk=product.pk)

        if score < 1 or score > 5:
            messages.error(request, "Invalid score.")
            return redirect('product-detail', pk=product.pk)

        rating, created = Rating.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={'score': score}
        )

        if created:
            messages.success(request, f"You rated {product.title} with {score} stars.")
        else:
            messages.success(request, f"Your rating for {product.title} has been updated to {score} stars.")

        return redirect('product-detail', pk=product.pk)



class FinalOrderListView(LoginRequiredMixin, ListView):
    model = FinalOrder
    context_object_name = 'final_orders'
    template_name = 'order/final_order_list.html'

    def get_queryset(self):
        return FinalOrder.objects.filter(user=self.request.user)\
                                 .prefetch_related(
                                     'orders__items__product__image_product'
                                 )