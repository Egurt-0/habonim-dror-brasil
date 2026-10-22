from django.db import models


class Termo(models.Model):
    termo = models.CharField("termo", max_length=80, help_text="Como aparece no glossário.")
    slug = models.SlugField("slug", max_length=80, unique=True)
    definicao = models.TextField("definição")
    variantes = models.CharField(
        "variantes",
        max_length=300,
        blank=True,
        help_text=(
            "Formas que devem ser destacadas no texto, separadas por vírgula "
            "(ex.: snif, snifim). Se vazio, usa o próprio termo."
        ),
    )

    class Meta:
        verbose_name = "termo"
        verbose_name_plural = "termos"
        ordering = ["termo"]

    def __str__(self):
        return self.termo

    def formas(self):
        """Palavras que, no texto corrido, devem apontar para este termo."""
        lista = [v.strip() for v in self.variantes.split(",") if v.strip()]
        return lista or [self.termo]
