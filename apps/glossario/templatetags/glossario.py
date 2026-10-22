from django import template

from ..services import texto_com_glossario

register = template.Library()


@register.filter
def com_glossario(texto):
    """Uso: {{ bloco.texto|com_glossario }}"""
    return texto_com_glossario(texto)
