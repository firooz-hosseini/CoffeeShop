from django.contrib import admin
from .models import *

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = ['image']
    max_num = 6


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'ingredient', 'price', 'quantity']
    search_fields = ['title', 'description']
    list_filter = ['category']
    inlines = [ImageInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']
    list_filter = ['product']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']
    search_fields = ['user__username', 'product__title']
    list_filter = ['product']

    
admin.site.register(Category)