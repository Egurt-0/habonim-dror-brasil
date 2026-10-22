from django.db import models


class Ordenavel(models.Model):
    ordem = models.PositiveSmallIntegerField("ordem", default=0)

    class Meta:
        abstract = True
        ordering = ["ordem"]


class Pilar(Ordenavel):
    """Um dos quatro pilares ideológicos."""

    nome = models.CharField("nome", max_length=80)
    slug = models.SlugField("slug", max_length=80, unique=True)
    subtitulo = models.CharField("subtítulo", max_length=80, blank=True)
    resumo = models.TextField("resumo", help_text="Uma ou duas frases, usadas nos cards.")
    texto = models.TextField("texto completo")

    class Meta(Ordenavel.Meta):
        verbose_name = "pilar"
        verbose_name_plural = "pilares"

    def __str__(self):
        return self.nome


class ReferenciaPedagogica(Ordenavel):
    """Referência da Torá Educativa (Paulo Freire, Korczak…)."""

    nome = models.CharField("nome", max_length=120)
    descricao = models.TextField("descrição")

    class Meta(Ordenavel.Meta):
        verbose_name = "referência pedagógica"
        verbose_name_plural = "referências pedagógicas"

    def __str__(self):
        return self.nome


class Tochnit(Ordenavel):
    """Etapa da jornada educacional (Solelim Beit, Bonim…) e seus temas."""

    nome = models.CharField("shichvá", max_length=80)
    temas = models.TextField("temas")

    class Meta(Ordenavel.Meta):
        verbose_name = "tochnit"
        verbose_name_plural = "tochniot"

    def __str__(self):
        return self.nome


class Numero(Ordenavel):
    """Número do movimento exibido no site (ex.: 'Cerca de 400' chaverim por semana)."""

    valor = models.CharField("valor", max_length=20, help_text="Ex.: 400, +15, 80")
    prefixo = models.CharField("prefixo", max_length=30, blank=True, help_text="Ex.: Cerca de")
    rotulo = models.CharField("rótulo", max_length=160)
    destaque = models.BooleanField("aparece na home", default=True)

    class Meta(Ordenavel.Meta):
        verbose_name = "número"
        verbose_name_plural = "números"

    def __str__(self):
        return f"{self.valor} {self.rotulo}"
