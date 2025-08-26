from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categories',views.CategoryViewSet, basename='category-api')
router.register('products', views.ProductViewSet, basename='product-api')
router.register('favorites', views.FavoriteViewSet, basename='favorite-api')
router.register('product-ingredients', views.ProductIngredientsViewSet, basename='product-ingredients-api')

urlpatterns = [
    path("", include(router.urls)),
]