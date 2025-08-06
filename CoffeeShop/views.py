from django.views.generic import TemplateView
from products.models import Product,Category
class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get('category')
        products = Product.objects.all()
        if category_id:
            products = products.filter(category_id=category_id)
        context['products'] = products
        context['categories'] = Category.objects.all()
        return context
