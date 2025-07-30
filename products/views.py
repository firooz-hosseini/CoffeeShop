from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from .models import Product,Favorite


@login_required
def add_to_favorites(request,product_id):
    product = get_object_or_404(Product,id = product_id)
    Favorite.objects.create(user = request.user,product = product)
    return redirect('product_detail',product_id=product.id)

@login_required
def user_favorites(request):
    favorite = Favorite.objects.filter(user = request.user)
    return render(request,'products/user_favorites.html',{'favorite':favorite})



