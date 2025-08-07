from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/',views.MyLoginView.as_view(next_page='home') , name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('password-reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='edit-profile'),
    path('profile/change-password/', views.CustomPasswordChangeView.as_view(), name='change-password'),


    


]