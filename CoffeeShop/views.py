from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['greeting'] = f'Hi dear {user.first_name}  👋'
        else:
            context['greeting'] = 'Hi guest, please login or register.'
        return context
