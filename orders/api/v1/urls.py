from rest_framework.routers import DefaultRouter
from .views import OrderViewSet,CommentViewSet,RatingViewSet,NotificationViewSet

router = DefaultRouter()
router.register('order',OrderViewSet,basename='order')
router.register('comment',CommentViewSet,basename='comment')
router.register('rating',RatingViewSet,basename='rating')
router.register('notification',NotificationViewSet,basename='rating')

urlpatterns = [router.urls]
