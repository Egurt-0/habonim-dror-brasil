from django.shortcuts import render

from apps.core.selectors import blocos

from .selectors import snif_da_pagina, snifim_ativos


def lista(request):
    contexto = {"blocos": blocos("snifim_intro"), "snifim": snifim_ativos()}
    return render(request, "snifim/lista.html", contexto)


def detalhe(request, slug):
    return render(request, "snifim/detalhe.html", {"snif": snif_da_pagina(slug)})


def quero_saber_mais(request):
    contexto = {
        "blocos": blocos("saber_mais_intro", "conta_nacional"),
        "snifim": snifim_ativos(),
    }
    return render(request, "snifim/quero_saber_mais.html", contexto)
