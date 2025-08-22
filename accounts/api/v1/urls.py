from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('', views.SignUpApiViewSet, basename='signup')
router.register('', views.VerifyOtpApiViewSet, basename='verify')
router.register('', views.LoginApiViewSet, basename='login')
router.register('', views.LogoutAPIViewSet, basename='logout')
router.register('', views.FullProfileViewSet, basename='full-profile')
router.register('', views.ProfileViewSet, basename='profile')
router.register('', views.FavoriteViewSet, basename='favorite')
router.register('', views.OrderViewSet, basename='orders')

urlpatterns = router.urls