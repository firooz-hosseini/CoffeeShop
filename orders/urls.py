from django.urls import path
from .views import CreateOrderView

urlpatterns = [
    path('order/create/<int:product_id>/', CreateOrderView.as_view(), name='create_order'),
]