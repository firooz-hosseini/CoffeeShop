from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def order_list(request):
    orders = Order.objects.all()
    category_id = request.GET.get("category")
    created_order = request.GET.get('time')
    start_date = request.GET.get('time')

    if category_id:
       orders = orders.filter(items__product__category__id=category_id)
    if created_order:
        orders = orders.filter(time__range=[start_date])

    return render(request,'order/order_list.html',{'orders':orders})
