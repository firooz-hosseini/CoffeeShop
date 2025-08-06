from django.contrib import admin, messages
from .models import Order, OrderItem, Rating, Comment, Notification
from django.core.cache import cache

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'time', 'seen_by_admin')
    list_filter = ('seen_by_admin', 'time', 'items__product__category')
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
    inlines = [OrderItemInline]




    def changelist_view(self, request, extra_context=None):
        new_orders = Order.objects.filter(seen_by_admin=False)
        count = new_orders.count()

        if count > 0:
            messages.warning(request, f"🔔{count} new order registered")
        return super().changelist_view(request, extra_context=extra_context)
    
    
    def save_model(self, request, obj, form, change):
        obj.seen_by_admin = True
        super().save_model(request, obj, form, change)
    


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


@admin.action(description="Mark selected notifications as read")
def mark_as_read(modeladmin, request, queryset):
    queryset.update(is_read=True)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('message',)
    ordering = ('-created_at',)
    actions = [mark_as_read]

