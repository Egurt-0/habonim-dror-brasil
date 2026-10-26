from itertools import count

from django.urls import reverse
from django.utils.html import escape, linebreaks
from django.utils.safestring import mark_safe

from .selectors import formas_do_glossario

# Cada definição precisa de um id único na página (aria-describedby); um contador basta.
_ids = count(1)


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
            id_def = f"termo-def-{next(_ids)}"
            partes.append(
                f'<a class="termo" href="{url}#{slug}" aria-describedby="{id_def}">'
                f"{escape(match.group(0))}"
                f'<span class="termo__definicao" id="{id_def}" role="tooltip" aria-hidden="true">'
                f"{escape(definicao)}</span></a>"
            )
            inicio = match.end()
        partes.append(escape(texto[inicio:]))
    else:
        partes.append(escape(texto))
    html = "".join(partes)
    return mark_safe(linebreaks(html) if paragrafos else html)
