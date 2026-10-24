from django.shortcuts import render

from apps.movimento.selectors import numeros_em_destaque

from .selectors import blocos, fotos_de_fundo, topicos_da_home

ARGUMENTOS = ["arg_capilaridade", "arg_alcance", "arg_impacto"]


def home(request):
    textos = blocos("home_hero", *ARGUMENTOS)
    contexto = {
        "blocos": textos,
        "argumentos": [textos[chave] for chave in ARGUMENTOS],
        "numeros": numeros_em_destaque(),
        "topicos": topicos_da_home(),
        "fotos_fundo": fotos_de_fundo(),
    }
    return render(request, "core/home.html", contexto)


SECOES_PRIVACIDADE = [
    "priv_intro",
    "priv_dados",
    "priv_fotos",
    "priv_compartilhamento",
    "priv_retencao",
    "priv_direitos",
]


def privacidade(request):
    textos = blocos(*SECOES_PRIVACIDADE, "priv_encarregado")
    datas = [b.updated_at for b in textos.values() if b.updated_at]
    contexto = {
        "blocos": textos,
        "secoes": [textos[chave] for chave in SECOES_PRIVACIDADE],
        "atualizada_em": max(datas, default=None),
    }
    return render(request, "core/privacidade.html", contexto)
