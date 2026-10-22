from django.urls import reverse
from django.utils.html import escape, linebreaks
from django.utils.safestring import mark_safe

from .selectors import formas_do_glossario


def texto_com_glossario(texto, paragrafos=True):
    """Liga a 1ª ocorrência de cada termo ao glossário e devolve HTML seguro.

    A busca é feita no texto original; cada trecho entre termos é escapado separadamente,
    então nada vindo do banco vira HTML. Com `paragrafos=True`, quebra em <p>; senão,
    devolve só o trecho (para usar dentro de <p>, <span> etc.).
    """
    texto = texto or ""
    formas, padrao = formas_do_glossario()
    partes = []
    if padrao:
        url = reverse("glossario:lista")
        ja_ligados = set()
        inicio = 0
        for match in padrao.finditer(texto):
            slug, definicao = formas[match.group(0).lower()]
            if slug in ja_ligados:
                continue
            ja_ligados.add(slug)
            partes.append(escape(texto[inicio : match.start()]))
            partes.append(
                f'<a class="termo" href="{url}#{slug}" data-definicao="{escape(definicao)}">'
                f"{escape(match.group(0))}</a>"
            )
            inicio = match.end()
        partes.append(escape(texto[inicio:]))
    else:
        partes.append(escape(texto))
    html = "".join(partes)
    return mark_safe(linebreaks(html) if paragrafos else html)
