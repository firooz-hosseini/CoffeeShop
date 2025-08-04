from django.shortcuts import render , get_object_or_404 , redirect , request
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.generic import ListView, DetailView


@login_required
def add_to_favorites(request,product_id):
    product = get_object_or_404(Product,id = product_id)
    Favorite.objects.create(user = request.user,product = product)
    return redirect('product-detail', pk=product.id)
   
@login_required
def user_favorites(request):
    favorite = Favorite.objects.filter(user = request.user)
    return render(request,'favorite/user_favorites.html',{'favorite':favorite})


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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'