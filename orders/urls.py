from django.urls import path
from .views import CreateOrderView
from . import views

urlpatterns = [
    path('order/create/<int:product_id>/', CreateOrderView.as_view(), name='create_order'),
      path('order/success/', views.order_success, name='order_success'),
]