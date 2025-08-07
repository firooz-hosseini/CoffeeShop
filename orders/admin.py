from django.contrib import admin
from .models import Order, OrderItem, Rating, Comment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'time', 'status']
    list_filter = ['time', 'items__product__category', 'status']
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    list_editable = ['status']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    search_fields = ['product__title', 'order__user__first_name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'text', 'is_approved', 'time']
    list_filter = ['is_approved', 'time']
    search_fields = ['user__first_name', 'product__title', 'text']

    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} comment(s) approved.")
    approve_comments.short_description = 'Approve selected comments'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'score']
    search_fields = ['user__first_name', 'product__title']