from rest_framework.routers import DefaultRouter
from .views import OrderViewSet,RatingViewSet,NotificationViewSet,KitchenOrderViewSet, PaymentViewSet
from django.urls import path,include

router = DefaultRouter()
router.register('order',OrderViewSet,basename='order')
router.register('rating',RatingViewSet,basename='rating')
router.register('notification',NotificationViewSet,basename='notification')
router.register('kitchen',KitchenOrderViewSet,basename='kitchen-order')
router.register('',PaymentViewSet,basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]
