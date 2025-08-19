from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .viewes import ProductViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path("", include(router.urls)),
]