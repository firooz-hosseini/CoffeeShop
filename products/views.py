from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from orders.forms import CommentForm
from orders.models import Comment
from products.models import Product

from .models import *


@login_required
def add_to_favorites(request,product_id):
    product = get_object_or_404(Product,id = product_id)
    Favorite.objects.create(user = request.user,product = product)
    messages.success(request, f'{product.title} is added to your favorite.')
    return redirect('product-detail', pk=product.pk)
   
@login_required
def user_favorites(request):
    favorite = Favorite.objects.filter(user = request.user)
    return render(request,'favorite/user_favorites.html',{'favorite':favorite})

@login_required
def remove_from_favorites(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Favorite.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f'{product.title} is removed from your favorite.')
    return redirect('product-detail', pk=product.pk)

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def product_list(request):
        category_id = request.GET.get('Category')
        categories = Category.objects.all()

        if category_id:
            products = Product.objects.filter(category_id=category_id)
        else:
            products = Product.objects.all()


        return render(request, 'product_list.html', {
            'products': products,
            'categories': categories,
            'selected_category': int(category_id) if category_id else None,
        })


class ProductDetailView(FormMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    form_class = CommentForm


    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.Comment_product.filter(is_approved=True).order_by('-time')
        
        if self.request.user.is_authenticated:
            context['form'] = self.get_form()
            context['is_favorite'] = Favorite.objects.filter(
                user=self.request.user, product=self.object
            ).exists()
        else:
            context['is_favorite'] = False

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect('login')

        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = self.object
            comment.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)