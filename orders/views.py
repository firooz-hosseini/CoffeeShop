from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from products.models import Product

from .forms import AddToCartForm
from .models import Comment, Notification, Order, CartItem, Rating,Cart


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if product.quantity <= 0:
            messages.error(request,'This product is out of stock.')
            return redirect('product-detail', pk=product.pk)
        
        form = AddToCartForm()
        return render(request, 'order/add_to_cart.html', {'form': form, 'product': product})

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if product.quantity <= 0:
            messages.error(request, "This product is out of stock.")
            return redirect('product-detail', pk=product.pk)

        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity > product.quantity:
                messages.error(request, f"Only {product.quantity} items are available.")
                return redirect('product-detail', pk=product.pk)

            cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
            cart_item, created_item = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created_item:
                cart_item.quantity += quantity
                cart_item.save()
            
            messages.success(request, f"{quantity} x {product.title} added to your cart.")

            return redirect('cart_detail')  
        return redirect('product-detail', pk=product.pk)

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    return render(request, 'order/cart_detail.html', {'cart': cart})

@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart_detail')
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user, is_paid=False)
    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_detail')

    if request.method == 'POST':
        cart.is_paid = True
        cart.save()

        order = Order.objects.create(user=request.user, cart=cart, status='paid')
        Notification.objects.create(message=f"New order by {request.user.first_name}")
        messages.success(request, "Order placed successfully!")
        return redirect('order_list')

    return render(request, 'order/checkout.html', {'cart': cart})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('cart__items__product')
    return render(request, 'order/order_list.html', {'orders': orders})

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
    return render(request, 'order/order_list.html', {'orders':orders})
 
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
    orders = Order.objects.filter(user=request.user, status='pending')

    if not orders.exists():
        messages.error(request, 'There is no order to pay!')
        return redirect('order_list')
      
    if request.method == 'POST':
        for order in orders:
            try:
                mark_as_paid(order)
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
