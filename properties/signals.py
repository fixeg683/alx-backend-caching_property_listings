from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

@receiver(post_save, sender=Property)
def invalidate_cache_on_save(sender, instance, **kwargs):
    """Invalidate cache when a Property is saved (created or updated)"""
    cache_key = 'all_properties'
    if cache.get(cache_key):
        cache.delete(cache_key)

@receiver(post_delete, sender=Property)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when a Property is deleted"""
    cache_key = 'all_properties'
    if cache.get(cache_key):
        cache.delete(cache_key)