from orders.models import Notification

def notifications(request):
    return {
        'notifications': Notification.objects.filter(is_read=False).order_by('-created_at')
    }