from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/',views.MyLoginView.as_view() , name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
        path('password-reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),


]