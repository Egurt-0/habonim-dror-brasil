from django.core.validators import RegexValidator
from django.db import models

VALIDADOR_LINK_INTERNO = RegexValidator(r"^/(?![/\\])", "Use um caminho interno, começando com /.")


class BlocoTexto(models.Model):
    """Trecho de texto institucional editável pelo admin.

    Os templates buscam o bloco pela `chave`; o texto aceita parágrafos separados por linha em
    branco, e termos do glossário são destacados automaticamente.
    """

    chave = models.SlugField("chave", max_length=80, unique=True)
    titulo = models.CharField("título", max_length=200, blank=True)
    texto = models.TextField("texto", blank=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "bloco de texto"
        verbose_name_plural = "blocos de texto"
        ordering = ["chave"]

    def __str__(self):
        return self.titulo or self.chave


class Topico(models.Model):
    """Bloco da grade de tópicos da home: título, frase curta e "Saiba mais".

    A foto vem de static/img/topicos/<slug>.<jpg|png|webp>; sem foto, o card fica vermelho.
    """

    titulo = models.CharField("título", max_length=80)
    slug = models.SlugField(
        "slug", max_length=80, unique=True, help_text="Também é o nome do arquivo da foto."
    )
    resumo = models.CharField("resumo", max_length=200)
    link = models.CharField(
        "link do Saiba mais",
        max_length=200,
        help_text="Caminho interno, ex.: /bases/#pilares",
        validators=[VALIDADOR_LINK_INTERNO],
    )
    ordem = models.PositiveSmallIntegerField("ordem", default=0)
    ativo = models.BooleanField("ativo", default=True)

    class Meta:
        verbose_name = "tópico da home"
        verbose_name_plural = "tópicos da home"
        ordering = ["ordem"]

    def __str__(self):
        return self.titulo
