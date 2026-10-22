import re
from functools import lru_cache

from django.core.cache import cache

from .models import Termo

CACHE_KEY_FORMAS = "glossario:formas"
CACHE_TIMEOUT = 300


def termos():
    return Termo.objects.all()


def formas_do_glossario():
    """Mapa {forma em minúsculas: (slug, definição)} e o padrão regex que reconhece as formas.

    O cache é limpo quando um termo muda. Com vários processos em produção e cache local,
    os outros processos podem levar até CACHE_TIMEOUT para ver a mudança.
    """
    dados = cache.get(CACHE_KEY_FORMAS)
    if dados is None:
        formas = {}
        for t in Termo.objects.all():
            for forma in t.formas():
                formas[forma.lower()] = (t.slug, t.definicao)
        padrao = ""
        if formas:
            alternativas = "|".join(re.escape(f) for f in sorted(formas, key=len, reverse=True))
            padrao = rf"(?<!\w)({alternativas})(?!\w)"
        dados = {"formas": formas, "padrao": padrao}
        cache.set(CACHE_KEY_FORMAS, dados, CACHE_TIMEOUT)
    return dados["formas"], compilar(dados["padrao"])


@lru_cache(maxsize=8)
def compilar(padrao):
    """Compila uma vez por padrão; o cache guarda só o texto do padrão."""
    return re.compile(padrao, re.IGNORECASE) if padrao else None
