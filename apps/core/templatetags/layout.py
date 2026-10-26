from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


class GuardarNode(template.Node):
    def __init__(self, nodelist, variavel):
        self.nodelist = nodelist
        self.variavel = variavel

    def render(self, context):
        # O conteúdo já sai escapado pelo autoescape; guardamos como seguro para não escapar 2x.
        context[self.variavel] = mark_safe(self.nodelist.render(context).strip())
        return ""


@register.tag
def guardar(parser, token):
    """Renderiza o trecho uma vez e guarda numa variável, para usar o mesmo bloco em vários lugares.

    Uso: {% guardar as titulo_pagina %}{% block titulo %}{% endblock %}{% endguardar %}
    """
    partes = token.split_contents()
    if len(partes) != 3 or partes[1] != "as":
        raise template.TemplateSyntaxError("Uso: {% guardar as nome %}...{% endguardar %}")
    nodelist = parser.parse(("endguardar",))
    parser.delete_first_token()
    return GuardarNode(nodelist, partes[2])


@register.filter
def absoluta(url):
    """'/static/x.png' → 'https://site/static/x.png'.

    Usa DJANGO_SITE_URL, nunca o Host da requisição (que pode ser forjado).
    """
    if not url or url.startswith(("http://", "https://")):
        return url
    return f"{settings.SITE_URL}{url}"
