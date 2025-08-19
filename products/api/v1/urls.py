from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter

from . import viewes
router = DefaultRouter()
router.register("",viewes.ProductViewSet),

urlpatterns = [
    path("", include(router.urls)),
]