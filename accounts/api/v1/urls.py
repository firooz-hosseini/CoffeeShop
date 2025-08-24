from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

from rest_framework_simplejwt.views import TokenRefreshView


router = DefaultRouter()
router.register('signup', views.SignUpApiViewSet, basename='signup')
router.register('verify_otp', views.VerifyOtpApiViewSet, basename='verify')
router.register('login', views.LoginApiViewSet, basename='login')
router.register('logout', views.LogoutAPIViewSet, basename='logout')
router.register('full-profile', views.FullProfileViewSet, basename='full-profile')
router.register('', views.ProfileViewSet, basename='profile')
router.register('', views.FavoriteViewSet, basename='favorite')
router.register('', views.OrderViewSet, basename='orders')

urlpatterns = router.urls + [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]