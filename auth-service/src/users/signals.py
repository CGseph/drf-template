from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
@receiver(post_delete, sender=User)
def invalidate_user_cache(sender, instance, **kwargs):
    cache.delete_pattern(f"*:retrieve:GET:api:users:{instance.id}*")
    cache.delete_pattern("*:list:GET:api:users*")
