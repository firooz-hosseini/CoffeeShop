from django.core.cache import cache

def new_order_notifications(request):
    return {
        'new_order_count': cache.get('new_order_count', 0)
    }
