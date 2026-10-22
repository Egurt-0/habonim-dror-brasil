"""Imagens colocadas em static/img/ são detectadas pelo nome, sem precisar de código.

- static/img/logos/<nome>.<ext>       → logos oficiais (ver context_processors.logos)
- static/img/fundos/*.<ext>           → fotos do fundo da home (trocam sozinhas)
- static/img/topicos/<slug>.<ext>     → foto de cada tópico da home
- static/img/paginas/<pagina>.<ext>   → foto do cabeçalho de cada página interna

Em desenvolvimento a busca é refeita a cada página (imagem nova aparece na hora). Em produção
o resultado fica em memória até o servidor reiniciar.
"""

from functools import lru_cache
from pathlib import Path

from django.conf import settings

EXTENSOES = (".svg", ".webp", ".jpg", ".jpeg", ".png")


def _pastas_estaticas():
    return [Path(p) for p in settings.STATICFILES_DIRS]


def _achar(caminho_sem_extensao):
    for pasta in _pastas_estaticas():
        for ext in EXTENSOES:
            if (pasta / f"{caminho_sem_extensao}{ext}").is_file():
                return f"{caminho_sem_extensao}{ext}"
    return None


def _listar(pasta_relativa):
    arquivos = set()
    for pasta in _pastas_estaticas():
        alvo = pasta / pasta_relativa
        if alvo.is_dir():
            for arquivo in alvo.iterdir():
                if arquivo.is_file() and arquivo.suffix.lower() in EXTENSOES:
                    arquivos.add(f"{pasta_relativa}/{arquivo.name}")
    return sorted(arquivos)


_achar_cacheado = lru_cache(maxsize=256)(_achar)
_listar_cacheado = lru_cache(maxsize=32)(_listar)


def achar(caminho_sem_extensao):
    """Caminho estático (ex.: 'img/logo.svg') do 1º arquivo com esse nome, ou None."""
    return (_achar if settings.DEBUG else _achar_cacheado)(caminho_sem_extensao)


def listar(pasta_relativa):
    """Caminhos estáticos de todas as imagens de uma pasta, em ordem alfabética."""
    return (_listar if settings.DEBUG else _listar_cacheado)(pasta_relativa)
