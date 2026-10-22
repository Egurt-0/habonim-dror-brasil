from django.core.cache import cache

from .models import Termo

CACHE_KEY_FORMAS = "glossario:formas"
CACHE_TIMEOUT = 300


def termos():
    return Termo.objects.all()


def formas_do_glossario():
    """Mapa {forma em minúsculas: (slug, definição)}.

    O cache é limpo quando um termo muda. Com vários processos em produção e cache local,
    os outros processos podem levar até CACHE_TIMEOUT para ver a mudança.
    """
    formas = cache.get(CACHE_KEY_FORMAS)
    if formas is None:
        formas = {}
        for t in Termo.objects.all():
            for forma in t.formas():
                formas[forma.lower()] = (t.slug, t.definicao)
        cache.set(CACHE_KEY_FORMAS, formas, CACHE_TIMEOUT)
    return formas
