import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_GET

from apps.movimento.selectors import numeros_em_destaque
from apps.snifim.selectors import snifim_ativos

from .context_processors import logos
from .movimento import ANO_FUNDACAO
from .selectors import blocos, fotos_de_fundo, topicos_da_home
from .templatetags.layout import absoluta

ARGUMENTOS = ["arg_capilaridade", "arg_alcance", "arg_impacto"]


def home(request):
    textos = blocos("home_hero", *ARGUMENTOS)
    contexto = {
        "blocos": textos,
        "argumentos": [textos[chave] for chave in ARGUMENTOS],
        "numeros": numeros_em_destaque(),
        "topicos": topicos_da_home(),
        "fotos_fundo": fotos_de_fundo(),
        "dados_estruturados": dados_estruturados(),
    }
    return render(request, "core/home.html", contexto)


def dados_estruturados():
    """JSON-LD "Organization" para o Google mostrar nome, logo e fundação do movimento."""
    dados = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Habonim Dror Brasil",
        "alternateName": "HDBR",
        "url": f"{settings.SITE_URL}/",
        "foundingDate": str(ANO_FUNDACAO),
        "description": (
            "Movimento juvenil judaico, sionista socialista, presente no Brasil desde 1945."
        ),
    }
    logo = logos()["completo"]
    if logo:
        dados["logo"] = absoluta(static(logo))
    # Escapa "<" para o JSON nunca fechar o <script> antes da hora.
    return mark_safe(json.dumps(dados, ensure_ascii=False).replace("<", r"\u003c"))


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


# Páginas públicas que vão para o sitemap (os snifim ativos entram automaticamente).
PAGINAS_DO_SITEMAP = [
    "core:home",
    "movimento:bases",
    "movimento:st",
    "movimento:sb",
    "movimento:kehila",
    "snifim:lista",
    "glossario:lista",
    "snifim:saber_mais",
    "core:privacidade",
]


@require_GET
def sitemap(request):
    urls = [reverse(nome) for nome in PAGINAS_DO_SITEMAP]
    urls += [
        reverse("snifim:detalhe", args=[slug])
        for slug in snifim_ativos().values_list("slug", flat=True)
    ]
    contexto = {"urls": [f"{settings.SITE_URL}{url}" for url in urls]}
    return render(request, "core/sitemap.xml", contexto, content_type="application/xml")


@require_GET
def robots(request):
    # O endereço do admin NÃO entra aqui: robots.txt é público e o revelaria.
    linhas = [
        "User-agent: *",
        "Disallow: /contas/",
        f"Sitemap: {settings.SITE_URL}{reverse('core:sitemap')}",
    ]
    texto = "".join(f"{linha}\n" for linha in linhas)
    return HttpResponse(texto, content_type="text/plain; charset=utf-8")
