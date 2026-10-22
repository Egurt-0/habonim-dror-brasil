from django.urls import reverse

from apps.contas.services import ja_escolheu_entrada

from . import imagens
from .selectors import blocos

SLOGAN_PADRAO = "80 anos formando líderes, construindo comunidade e conectando gerações."


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


def site(request):
    return {
        "menu": [
            ("Bases", reverse("movimento:bases")),
            ("Shichavot Tzeirot", reverse("movimento:st")),
            ("Shichavot Bogrot", reverse("movimento:sb")),
            ("Kehilá HD", reverse("movimento:kehila")),
            ("Glossário", reverse("glossario:lista")),
        ],
        "ja_escolheu_entrada": ja_escolheu_entrada(request),
        "slogan": blocos("slogan")["slogan"].titulo or SLOGAN_PADRAO,
        "logos": logos(),
    }
