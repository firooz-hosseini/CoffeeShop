from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/',LoginView.as_view() , name='login'),
    path('profile/', views.profile, name='profile'),


]