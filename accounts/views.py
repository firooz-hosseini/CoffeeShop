from django.shortcuts import render

from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')


class MyLoginView(LoginView):
    template_name = 'accounts/login.html'

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')