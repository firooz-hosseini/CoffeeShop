from django.urls import path

from . import views

urlpatterns = [
    path('favorite/add/<int:product_id>/',views.add_to_favorites,name='add-to-favorites'),
    path('favorites/',views.user_favorites,name='user_favorites'),
    path('remove-favorites/<int:pk>/',views.remove_from_favorites,name='remove-favorites'),
    path('product-list/', views.ProductListView.as_view(), name='product-list'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'), 
]