from django.urls import path
from .views import CreateOrderView
from . import views

urlpatterns = [
    path('create/<int:product_id>/', CreateOrderView.as_view(), name='create_order'),
    path('success/', views.order_success, name='order_success'),
    path('my-orders/', views.OrderListView.as_view(), name='order_list'),
    path('canceled/<int:order_id>', views.cancel_order_view, name='canceled_order'),
    path('delivered/<int:order_id>', views.deliver_order_view, name='delivered_order')
]