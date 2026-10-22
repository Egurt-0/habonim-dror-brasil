from django.urls import reverse

from apps.contas.services import ja_escolheu_entrada


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
    }
