from django import template

from .. import movimento

register = template.Library()


@register.filter
def com_anos(texto):
    """Uso: {{ "Há {anos} anos no Brasil"|com_anos }} → idade do movimento no ano atual."""
    return movimento.com_anos(texto)
