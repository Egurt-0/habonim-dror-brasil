from django.urls import reverse

from apps.contas.services import ja_escolheu_entrada

from . import imagens
from .movimento import anos_de_movimento, com_anos
from .selectors import blocos

SLOGAN_PADRAO = "{anos} anos formando líderes, construindo comunidade e conectando gerações."


def logos():
    """Arquivos oficiais em static/img/logos/ (None quando o arquivo não existe).

    - semel: estrela vermelha, usada no topo (sobre branco)
    - semel_branco: estrela branca, usada sobre foto ou vermelho
    - completo: estrela + "Habonim Dror Brasil"
    - icone: semel no círculo vermelho, ícone da aba
    """
    return {
        "semel": imagens.achar("img/logos/semel"),
        "semel_branco": imagens.achar("img/logos/semel-branco"),
        "completo": imagens.achar("img/logos/logo-completo"),
        "icone": imagens.achar("img/logos/semel-circulo"),
    }


def _item(rotulo, url, request):
    return {"rotulo": rotulo, "url": url, "atual": request.path == url}


def menu(request):
    """Menu do topo (e do rodapé). Item com "filhos" vira submenu: o rótulo abre a lista."""
    shichavot = [
        _item("Tzeirot (ST)", reverse("movimento:st"), request),
        _item("Bogrot (SB)", reverse("movimento:sb"), request),
    ]
    return [
        _item("Bases", reverse("movimento:bases"), request),
        {
            "rotulo": "Shichavot",
            "filhos": shichavot,
            "atual": any(filho["atual"] for filho in shichavot),
        },
        _item("Kehilá HD", reverse("movimento:kehila"), request),
        _item("Snifim", reverse("snifim:lista"), request),
        _item("Glossário", reverse("glossario:lista"), request),
    ]


def site(request):
    return {
        "menu": menu(request),
        "ja_escolheu_entrada": ja_escolheu_entrada(request),
        "slogan": blocos("slogan")["slogan"].titulo or com_anos(SLOGAN_PADRAO),
        "anos_de_movimento": anos_de_movimento(),
        "logos": logos(),
        # Imagem dos links compartilhados (WhatsApp, Instagram…): static/img/compartilhar.jpg,
        # de preferência 1200×630; sem ela, a logo completa.
        "imagem_compartilhar": imagens.achar("img/compartilhar") or logos()["completo"],
    }
