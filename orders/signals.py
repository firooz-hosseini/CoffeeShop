from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order, FinalOrder


@receiver(post_save, sender=FinalOrder)
def notify_admin_on_new_order(sender, instance, created, **kwargs):
    if created:
        new_orders = cache.get('new_order_count', 0)
        cache.set('new_order_count', new_orders + 1)