from django.contrib import admin
from .models import Order, OrderItem, Rating, Comment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'time', 'status')
    list_filter = ('time', 'items__product__category', 'status')
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    search_fields = ['product__title', 'order__user__first_name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'text', 'is_approved', 'time')
    list_filter = ('is_approved', 'time')
    search_fields = ('user__first_name', 'product__title', 'text')

    action = ['approve_comment']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'score']
    search_fields = ['user__first_name', 'product__title']