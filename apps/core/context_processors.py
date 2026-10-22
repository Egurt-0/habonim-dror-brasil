from django.urls import reverse

from apps.contas.services import ja_escolheu_entrada

from .selectors import blocos

SLOGAN_PADRAO = "80 anos formando líderes, construindo comunidade e conectando gerações."


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
    }
