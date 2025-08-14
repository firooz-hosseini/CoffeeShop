from django.urls import path

from . import views
from .views import CommentCreateView, CreateOrderView

urlpatterns = [
    path('create/<int:product_id>/', CreateOrderView.as_view(), name='create_order'),
    path('my-orders/', views.OrderListView.as_view(), name='order_list'),
    path('comment/add/<int:product_id>/', CommentCreateView.as_view(), name='add_comment'),
    path('cancel/<int:order_id>/', views.cancel_order_view, name='cancel_order'),
    path('delete/<int:order_id>/', views.delete_order_view, name='delete_order'),
    path('pay/<int:order_id>/', views.pay_order_views, name='order_pay'),
    path('rate/<int:product_id>/', views.RateProductView.as_view(), name='rate_product'),
