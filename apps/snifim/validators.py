from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

TAMANHO_MAXIMO_MB = 8
EXTENSOES = ["jpg", "jpeg", "png", "webp"]

_extensao = FileExtensionValidator(EXTENSOES, message="Envie a foto em JPG, PNG ou WEBP.")


def validar_imagem(arquivo):
    """Tipo e tamanho do upload. O conteúdo de imagem é conferido pelo próprio ImageField."""
    _extensao(arquivo)
    if arquivo.size > TAMANHO_MAXIMO_MB * 1024 * 1024:
        raise ValidationError(f"A foto passa de {TAMANHO_MAXIMO_MB} MB. Diminua antes de enviar.")
