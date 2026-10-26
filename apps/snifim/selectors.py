from itertools import groupby

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from .models import Bagrut, FotoSnif, Kehila, Snif


def snifim_ativos():
    return Snif.objects.filter(ativo=True).select_related("kehila")


def snif_da_pagina(slug):
    """Snif ativo com a galeria e a Bagrut atual já carregadas; 404 se não houver.

    Atributos extras: `.galeria` (só fotos autorizadas) e `.bagrut_atual` (Bagrut ou None).
    """
    snif = get_object_or_404(
        snifim_ativos().prefetch_related(
            Prefetch("fotos", queryset=FotoSnif.objects.filter(autorizada=True), to_attr="galeria"),
            Prefetch("bagrutot", queryset=Bagrut.objects.filter(atual=True), to_attr="_atuais"),
        ),
        slug=slug,
    )
    snif.bagrut_atual = snif._atuais[0] if snif._atuais else None
    return snif


def kehilot_parceiras():
    return Kehila.objects.filter(snifim__ativo=True).distinct()


def linha_do_tempo():
    """Lista de (ano, [snifim fundados naquele ano]), do mais antigo ao mais novo."""
    snifim = snifim_ativos().order_by("ano_fundacao", "ordem", "nome")
    return [(ano, list(grupo)) for ano, grupo in groupby(snifim, key=lambda s: s.ano_fundacao)]
