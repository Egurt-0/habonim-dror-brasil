from django.db import models


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
