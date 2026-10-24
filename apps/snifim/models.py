from django.db import models, transaction
from django.urls import reverse

from .validators import validar_imagem


def _caminho(instancia, pasta, nome_arquivo):
    """Uploads ficam em media/snifim/<slug do snif>/<pasta>/."""
    snif = instancia if isinstance(instancia, Snif) else instancia.snif
    return f"snifim/{snif.slug}/{pasta}/{nome_arquivo}"


# Funções nomeadas no módulo: as migrations precisam conseguir importá-las.
def caminho_capa(instancia, nome_arquivo):
    return _caminho(instancia, "capa", nome_arquivo)


def caminho_galeria(instancia, nome_arquivo):
    return _caminho(instancia, "galeria", nome_arquivo)


def caminho_miniatura(instancia, nome_arquivo):
    return _caminho(instancia, "miniaturas", nome_arquivo)


def caminho_bagrut(instancia, nome_arquivo):
    return _caminho(instancia, "bagrut", nome_arquivo)


AJUDA_SEM_NOMES_DE_MENORES = (
    "Não escreva nomes de menores de idade sem autorização dos responsáveis (LGPD)."
)

AJUDA_AUTORIZACAO = (
    "Marque só se todas as pessoas da foto (ou os responsáveis, no caso de menores) "
    "autorizaram a publicação. Sem essa marcação, a foto não aparece no site."
)


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
    """Núcleo local da tnuá em uma cidade, com página própria em /snifim/<slug>/."""

    nome = models.CharField("nome", max_length=80, help_text="Ex.: Porto Alegre")
    slug = models.SlugField("slug", max_length=80, unique=True)
    cidade = models.CharField("cidade", max_length=80)
    estado = models.CharField("UF", max_length=2)
    ano_fundacao = models.PositiveSmallIntegerField("ano de fundação")
    resumo = models.CharField(
        "resumo",
        max_length=200,
        blank=True,
        help_text="Uma frase para o card na lista de snifim.",
    )
    historia = models.TextField(
        "história",
        blank=True,
        help_text="Separe os parágrafos com uma linha em branco.",
    )
    instagram = models.CharField(
        "Instagram", max_length=60, blank=True, help_text="Só o usuário, sem @."
    )
    contato = models.CharField(
        "contato",
        max_length=160,
        blank=True,
        help_text=(
            "E-mail ou WhatsApp institucional do snif (aparece no site). Nunca o número "
            "pessoal de um chanich ou madrich menor de idade."
        ),
    )
    endereco = models.CharField("endereço", max_length=200, blank=True)
    kehila = models.ForeignKey(
        Kehila,
        verbose_name="kehilá parceira",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="snifim",
    )
    tem_cchd = models.BooleanField("tem CCHD", default=False)
    cchd_descricao = models.TextField(
        "sobre a CCHD",
        blank=True,
        help_text="Texto sobre a Casa de Cultura Habonim Dror (só aparece se tiver CCHD).",
    )
    foto_capa = models.ImageField(
        "foto de capa",
        upload_to=caminho_capa,
        blank=True,
        validators=[validar_imagem],
        help_text="Horizontal, de preferência 1920×800. Sem foto, o topo fica vermelho.",
    )
    foto_capa_alt = models.CharField(
        "descrição da foto de capa",
        max_length=200,
        blank=True,
        help_text="O que aparece na foto (para leitores de tela).",
    )
    ativo = models.BooleanField("ativo", default=True)

    class Meta:
        verbose_name = "snif"
        verbose_name_plural = "snifim"
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        from .services import preparar_foto_capa

        preparar_foto_capa(self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("snifim:detalhe", args=[self.slug])

    @property
    def capa_url(self):
        return self.foto_capa.url if self.foto_capa else ""

    @property
    def instagram_url(self):
        return f"https://www.instagram.com/{self.instagram}/" if self.instagram else ""


class FotoSnif(models.Model):
    """Foto da galeria de um snif."""

    snif = models.ForeignKey(Snif, on_delete=models.CASCADE, related_name="fotos")
    imagem = models.ImageField("imagem", upload_to=caminho_galeria, validators=[validar_imagem])
    miniatura = models.ImageField(upload_to=caminho_miniatura, blank=True, editable=False)
    alt = models.CharField(
        "descrição da imagem",
        max_length=200,
        help_text="O que aparece na foto (para leitores de tela). Ex.: chanichim em roda.",
    )
    legenda = models.CharField(
        "legenda", max_length=200, blank=True, help_text=AJUDA_SEM_NOMES_DE_MENORES
    )
    data = models.DateField("data", null=True, blank=True)
    ordem = models.PositiveSmallIntegerField("ordem", default=0)
    autorizada = models.BooleanField(
        "publicação autorizada", default=False, help_text=AJUDA_AUTORIZACAO
    )

    class Meta:
        verbose_name = "foto da galeria"
        verbose_name_plural = "galeria"
        ordering = ["ordem", "-data", "id"]

    def __str__(self):
        return self.legenda or self.alt

    def save(self, *args, **kwargs):
        from .services import preparar_foto_galeria

        preparar_foto_galeria(self)
        super().save(*args, **kwargs)


class Bagrut(models.Model):
    """Grupo que gerencia o snif em uma gestão. O histórico fica guardado; o site mostra a atual."""

    snif = models.ForeignKey(Snif, on_delete=models.CASCADE, related_name="bagrutot")
    gestao = models.CharField("gestão", max_length=40, help_text="Ex.: 2026 ou 2025/2026")
    descricao = models.TextField("descrição", blank=True, help_text=AJUDA_SEM_NOMES_DE_MENORES)
    foto = models.ImageField(
        "foto", upload_to=caminho_bagrut, blank=True, validators=[validar_imagem]
    )
    foto_alt = models.CharField("descrição da foto", max_length=200, blank=True)
    autorizada = models.BooleanField(
        "publicação da foto autorizada", default=False, help_text=AJUDA_AUTORIZACAO
    )
    atual = models.BooleanField(
        "Bagrut atual",
        default=False,
        help_text="Só uma por snif. Marcar esta desmarca a anterior.",
    )

    class Meta:
        verbose_name = "Bagrut"
        verbose_name_plural = "Bagrutot"
        ordering = ["-gestao"]
        constraints = [
            models.UniqueConstraint(
                fields=["snif"],
                condition=models.Q(atual=True),
                name="uma_bagrut_atual_por_snif",
            )
        ]

    def __str__(self):
        return f"Bagrut {self.gestao} · {self.snif}"

    def save(self, *args, **kwargs):
        from .services import preparar_foto_bagrut

        preparar_foto_bagrut(self)
        # Desmarcar a anterior e salvar juntos: se o save falhar, o snif não fica sem Bagrut atual.
        with transaction.atomic():
            if self.atual:
                Bagrut.objects.filter(snif=self.snif, atual=True).exclude(pk=self.pk).update(
                    atual=False
                )
            super().save(*args, **kwargs)

    def validate_constraints(self, exclude=None):
        # A regra "uma atual por snif" é garantida no save() (desmarca a anterior) e no banco.
        # Validar aqui impediria trocar a Bagrut atual pelo admin.
        exclude = set(exclude or ()) | {"snif"}
        super().validate_constraints(exclude=exclude)
