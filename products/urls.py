from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('favorite/add/<int:product_id>/',views.add_to_favorites,name='add-to-favorites'),
    path('favorites/',views.user_favorites,name='user_favorites'),
    path('product-list/', views.ProductListView.as_view(), name='product-list'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'), 
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)