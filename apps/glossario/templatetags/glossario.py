from django import template

from ..services import texto_com_glossario

register = template.Library()


@register.filter
def com_glossario(texto):
    """Texto longo, quebrado em parágrafos. Uso: <div>{{ bloco.texto|com_glossario }}</div>"""
    return texto_com_glossario(texto)


@register.filter
def com_glossario_inline(texto):
    """Texto curto, sem <p>. Uso: <p>{{ tochnit.temas|com_glossario_inline }}</p>"""
    return texto_com_glossario(texto, paragrafos=False)
