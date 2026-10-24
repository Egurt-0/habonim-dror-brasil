"""Tratamento das fotos enviadas pelo admin: reduz o tamanho e gera miniaturas.

Só age quando chega um arquivo novo (ainda não salvo no storage), então editar a legenda
de uma foto não reprocessa a imagem.
"""

from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

LADO_MAXIMO = 1920
LADO_MINIATURA = 640


def _arquivo_novo(campo):
    return bool(campo) and not getattr(campo, "_committed", True)


def _redimensionar(campo, lado):
    """ContentFile JPEG/PNG com o maior lado limitado a `lado`, respeitando a rotação EXIF."""
    campo.seek(0)
    with Image.open(campo) as original:
        imagem = ImageOps.exif_transpose(original)
        imagem.thumbnail((lado, lado))
        tem_transparencia = imagem.mode in ("RGBA", "LA", "P")
        formato, ext = ("PNG", ".png") if tem_transparencia else ("JPEG", ".jpg")
        if formato == "JPEG" and imagem.mode != "RGB":
            imagem = imagem.convert("RGB")
        saida = BytesIO()
        opcoes = {"quality": 85, "optimize": True} if formato == "JPEG" else {"optimize": True}
        imagem.save(saida, formato, **opcoes)
    nome = Path(campo.name).stem + ext
    return nome, ContentFile(saida.getvalue())


def _reduzir(campo):
    nome, conteudo = _redimensionar(campo, LADO_MAXIMO)
    campo.save(nome, conteudo, save=False)


def preparar_foto_galeria(foto):
    if not _arquivo_novo(foto.imagem):
        return
    nome, miniatura = _redimensionar(foto.imagem, LADO_MINIATURA)
    _reduzir(foto.imagem)
    foto.miniatura.save(nome, miniatura, save=False)


def preparar_foto_bagrut(bagrut):
    if _arquivo_novo(bagrut.foto):
        _reduzir(bagrut.foto)


def preparar_foto_capa(snif):
    if _arquivo_novo(snif.foto_capa):
        _reduzir(snif.foto_capa)
