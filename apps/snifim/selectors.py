from itertools import groupby

from .models import Kehila, Snif


def snifim_ativos():
    return Snif.objects.filter(ativo=True).select_related("kehila")


def kehilot_parceiras():
    return Kehila.objects.filter(snifim__ativo=True).distinct()


def linha_do_tempo():
    """Lista de (ano, [snifim fundados naquele ano]), do mais antigo ao mais novo."""
    snifim = snifim_ativos().order_by("ano_fundacao", "nome")
    return [(ano, list(grupo)) for ano, grupo in groupby(snifim, key=lambda s: s.ano_fundacao)]
