from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from .models import Product,Favorite
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

@login_required
def remove_from_favorites(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Favorite.objects.filter(user=request.user, product=product).delete()
    return redirect('home')

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'