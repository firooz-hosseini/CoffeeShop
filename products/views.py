from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from .models import Product,Favorite
from django.views.generic import ListView, DetailView
from .models import Comment  
from django.contrib import messages  

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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


@login_required  
def add_comment(request, product_id): 
    product = get_object_or_404(Product, id=product_id)  
    purchased = check_user_purchased(request.user, product)  

    if request.method == 'POST':  
        text = request.POST.get('text')  
        rating = int(request.POST.get('rating', 0))  
        Comment.objects.create(  
            user=request.user,  
            product=product,  
            text=text,  
            rating=rating,  
            purchased=purchased,  
        )  
        messages.success(request, 'نظر شما با موفقیت ثبت شد.') 
        return redirect('product-detail', pk=product.id)