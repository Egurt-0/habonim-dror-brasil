from . import imagens
from .models import BlocoTexto, Topico
from .movimento import com_anos


class _Blocos(dict):
    """Dict de blocos por chave. Chave ausente devolve um bloco vazio em vez de quebrar."""

    def __missing__(self, chave):
        return BlocoTexto(chave=chave)


def blocos(*chaves):
    """Blocos por chave, com o marcador {anos} já trocado pela idade do movimento."""
    resultado = _Blocos()
    for b in BlocoTexto.objects.filter(chave__in=chaves):
        b.titulo, b.texto = com_anos(b.titulo), com_anos(b.texto)
        resultado[b.chave] = b
    return resultado


def topicos_da_home():
    """Tópicos ativos, com {anos} trocado e `.foto` (caminho estático ou None)."""
    topicos = list(Topico.objects.filter(ativo=True))
    for t in topicos:
        t.titulo, t.resumo = com_anos(t.titulo), com_anos(t.resumo)
        t.foto = imagens.achar(f"img/topicos/{t.slug}")
    return topicos


def fotos_de_fundo():
    return imagens.listar("img/fundos")
