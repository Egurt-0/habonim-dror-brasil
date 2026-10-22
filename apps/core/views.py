from django.shortcuts import render

from apps.movimento.selectors import numeros_em_destaque

from .selectors import blocos

ARGUMENTOS = ["arg_capilaridade", "arg_alcance", "arg_impacto"]


def home(request):
    textos = blocos("home_hero", *ARGUMENTOS)
    contexto = {
        "blocos": textos,
        "argumentos": [textos[chave] for chave in ARGUMENTOS],
        "numeros": numeros_em_destaque(),
    }
    return render(request, "core/home.html", contexto)
