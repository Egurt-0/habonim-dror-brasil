from django.shortcuts import render

from apps.core.selectors import blocos

from .selectors import termos


def lista(request):
    return render(
        request,
        "glossario/lista.html",
        {"termos": termos(), "blocos": blocos("glossario_intro")},
    )
