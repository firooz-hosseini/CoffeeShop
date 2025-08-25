from django.contrib import admin, messages
from django.core.cache import cache

from .models import Comment, Notification, Order, OrderItem, Rating


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'time', 'status', 'seen_by_admin']
    list_filter = ['time', 'items__product__category', 'status', 'seen_by_admin']
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    list_editable = ['status']
    
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