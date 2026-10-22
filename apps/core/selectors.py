from .models import BlocoTexto


class _Blocos(dict):
    """Dict de blocos por chave. Chave ausente devolve um bloco vazio em vez de quebrar."""

    def __missing__(self, chave):
        return BlocoTexto(chave=chave)


def blocos(*chaves):
    return _Blocos({b.chave: b for b in BlocoTexto.objects.filter(chave__in=chaves)})
