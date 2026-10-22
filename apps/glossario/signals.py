from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Termo
from .selectors import CACHE_KEY_FORMAS


@receiver([post_save, post_delete], sender=Termo)
def limpar_cache(**kwargs):
    cache.delete(CACHE_KEY_FORMAS)
