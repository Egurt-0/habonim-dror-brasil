from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from PIL import Image, UnidentifiedImageError

TAMANHO_MAXIMO_MB = 8
# Uma foto pequena em MB pode ter dimensões enormes e ocupar muita memória ao ser aberta.
# 50 MP cobre câmeras de celular (ex.: 8160×6120) e recusa imagens feitas para travar o servidor.
PIXELS_MAXIMO = 50_000_000
EXTENSOES = ["jpg", "jpeg", "png", "webp"]

# Freio de segurança do próprio Pillow: acima do dobro deste valor ele se recusa a abrir.
Image.MAX_IMAGE_PIXELS = PIXELS_MAXIMO

_extensao = FileExtensionValidator(EXTENSOES, message="Envie a foto em JPG, PNG ou WEBP.")


def _conferir_dimensoes(arquivo):
    """Lê só o cabeçalho da imagem (não carrega os pixels) para saber largura × altura."""
    arquivo.seek(0)
    try:
        with Image.open(arquivo) as imagem:
            pixels = imagem.width * imagem.height
    except Image.DecompressionBombError:
        pixels = PIXELS_MAXIMO + 1
    except (UnidentifiedImageError, OSError):
        raise ValidationError("O arquivo não é uma imagem válida.") from None
    finally:
        arquivo.seek(0)
    if pixels > PIXELS_MAXIMO:
        raise ValidationError(
            "As dimensões da foto são grandes demais. Reduza para no máximo 8000 px "
            "no lado maior antes de enviar."
        )


def validar_imagem(arquivo):
    """Tipo, tamanho e dimensões do upload. O ImageField também confere se é uma imagem."""
    _extensao(arquivo)
    if arquivo.size > TAMANHO_MAXIMO_MB * 1024 * 1024:
        raise ValidationError(f"A foto passa de {TAMANHO_MAXIMO_MB} MB. Diminua antes de enviar.")
    # Foto que já estava salva foi conferida no envio; não precisa abrir de novo.
    if not getattr(arquivo, "_committed", False):
        _conferir_dimensoes(arquivo)
