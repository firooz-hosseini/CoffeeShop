from django.urls import path
from . import views
from .views import CommentCreateView, AddToCartView

urlpatterns = [
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),  # ← نام استاندارد
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.order_list, name='order_list'),
    path('comment/add/<int:product_id>/', CommentCreateView.as_view(), name='add_comment'),
    path('cancel/<int:order_id>/', views.cancel_order_view, name='cancel_order'),
    path('delete/<int:order_id>/', views.delete_order_view, name='delete_order'),
    path('pay/', views.pay_order_views, name='order_pay'),
    path('rate/<int:product_id>/', views.RateProductView.as_view(), name='rate_product'),
]
