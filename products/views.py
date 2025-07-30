from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from .models import Product,Favorite
from django.views.generic import ListView, DetailView


@login_required
def add_to_favorites(request,product_id):
    product = get_object_or_404(Product,id = product_id)
    Favorite.objects.create(user = request.user,product = product)
    return redirect('product_detail',product_id=product.id)

@login_required
def user_favorites(request):
    favorite = Favorite.objects.filter(user = request.user)
    return render(request,'products/user_favorites.html',{'favorite':favorite})


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.prefetch_related('ingredient', 'image_product', 'category')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'