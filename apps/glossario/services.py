import re

from django.urls import reverse
from django.utils.html import escape, linebreaks
from django.utils.safestring import mark_safe

from .selectors import formas_do_glossario


def texto_com_glossario(texto):
    """Escapa o texto, quebra em parágrafos e liga a 1ª ocorrência de cada termo ao glossário.

    O resultado é HTML seguro: todo conteúdo vindo do banco é escapado antes de receber
    as marcações do glossário.
    """
    html = escape(texto or "")
    formas = formas_do_glossario()
    if formas:
        url = reverse("glossario:lista")
        padrao = re.compile(
            r"(?<!\w)("
            + "|".join(re.escape(f) for f in sorted(formas, key=len, reverse=True))
            + r")(?!\w)",
            re.IGNORECASE,
        )
        ja_ligados = set()

        def ligar(match):
            slug, definicao = formas[match.group(0).lower()]
            if slug in ja_ligados:
                return match.group(0)
            ja_ligados.add(slug)
            return (
                f'<a class="termo" href="{url}#{slug}" data-definicao="{escape(definicao)}">'
                f"{match.group(0)}</a>"
            )

        html = padrao.sub(ligar, html)
    return mark_safe(linebreaks(html))
