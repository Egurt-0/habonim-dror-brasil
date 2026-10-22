from django.shortcuts import render

from apps.core.selectors import blocos

from .selectors import snifim_ativos


def quero_saber_mais(request):
    contexto = {
        "blocos": blocos("saber_mais_intro", "conta_nacional", "slogan"),
        "snifim": snifim_ativos(),
    }
    return render(request, "snifim/quero_saber_mais.html", contexto)
