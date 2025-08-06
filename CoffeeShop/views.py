from django.views.generic import TemplateView
from products.models import Product,Category,Favorite
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
        if self.request.user.is_authenticated:
            favorite_ids = Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True)
            context['favorite_product_ids'] = list(favorite_ids)
        else:
            context['favorite_product_ids'] = []
        return context
