from django.contrib import admin
from .models import Product, Category, Ingredient, Favorite, Image

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category', 'ingredient')  

admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Favorite)
admin.site.register(Image)

