from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from .models import Product,Favorite


@login_required
def ad_to_favorites(request,prdoct_id):
    product = get_object_or_404(Product,id = prdoct_id)
    Favorite.objects.create(user = request.user,product = product)
    return redirect('product_detail',prdoct_id=product.id)

@login_required
def user_favorites(request):
    favorite = Favorite.objects.filter(user = request.user)
    return render(request,'products/user_favorites.html',{'favorite':favorite})



