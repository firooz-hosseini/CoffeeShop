from django.urls import path
from . import views

urlpatterns = [
    path('favorite/add/<int:product_id>/',views.add_to_favorites,name='add_to_favorites'),
    path('favorites/',views.user_favorites,name='user_favorites')
]