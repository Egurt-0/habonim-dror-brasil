from django.db import models


class Kehila(models.Model):
    """Comunidade judaica parceira de um snif."""

    nome = models.CharField("nome", max_length=160)
    cidade = models.CharField("cidade", max_length=80)
    site = models.URLField("site", blank=True)

    class Meta:
        verbose_name = "kehilá"
        verbose_name_plural = "kehilot"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Snif(models.Model):
    """Núcleo local da tnuá em uma cidade.

    Fase 1 guarda o básico. A fase 2 acrescenta história, galeria e Bagrut.
    """

    nome = models.CharField("nome", max_length=80, help_text="Ex.: Porto Alegre")
    slug = models.SlugField("slug", max_length=80, unique=True)
    cidade = models.CharField("cidade", max_length=80)
    estado = models.CharField("UF", max_length=2)
    ano_fundacao = models.PositiveSmallIntegerField("ano de fundação")
    instagram = models.CharField(
        "Instagram", max_length=60, blank=True, help_text="Só o usuário, sem @."
    )
    kehila = models.ForeignKey(
        Kehila,
        verbose_name="kehilá parceira",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="snifim",
    )
    tem_cchd = models.BooleanField("tem CCHD", default=False)
    ativo = models.BooleanField("ativo", default=True)

    class Meta:
        verbose_name = "snif"
        verbose_name_plural = "snifim"
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    @property
    def instagram_url(self):
        return f"https://www.instagram.com/{self.instagram}/" if self.instagram else ""
