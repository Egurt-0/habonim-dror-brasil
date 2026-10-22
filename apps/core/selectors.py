from . import imagens
from .models import BlocoTexto, Topico


class _Blocos(dict):
    """Dict de blocos por chave. Chave ausente devolve um bloco vazio em vez de quebrar."""

    def __missing__(self, chave):
        return BlocoTexto(chave=chave)


def blocos(*chaves):
    return _Blocos({b.chave: b for b in BlocoTexto.objects.filter(chave__in=chaves)})


def topicos_da_home():
    """Tópicos ativos, cada um com `.foto` (caminho estático ou None)."""
    topicos = list(Topico.objects.filter(ativo=True))
    for t in topicos:
        t.foto = imagens.achar(f"img/topicos/{t.slug}")
    return topicos


def fotos_de_fundo():
    return imagens.listar("img/fundos")
