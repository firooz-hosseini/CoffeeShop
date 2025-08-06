from django.urls import path
from .views import CreateOrderView
from . import views

urlpatterns = [
  
    path('create/<int:product_id>/', CreateOrderView.as_view(), name='create_order'),
    path('success/', views.order_success, name='order_success'),
    path('my-orders/', views.OrderListView.as_view(), name='order_list'),
    path('cancel/<int:order_id>/', views.cancel_order_view, name='cancel_order'),
    path('delete/<int:order_id>/', views.delete_order_view, name='delete_order'),
]