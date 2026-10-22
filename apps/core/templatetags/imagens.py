from django import template

from .. import imagens

register = template.Library()


@register.simple_tag
def foto_da_pagina(pagina):
    """Uso: {% foto_da_pagina "bases" as foto %} → 'img/paginas/bases.jpg' ou None."""
    return imagens.achar(f"img/paginas/{pagina}")
