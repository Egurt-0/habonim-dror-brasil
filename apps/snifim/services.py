"""Tratamento das fotos enviadas pelo admin: reduz o tamanho, gera miniaturas e apaga da
pasta media os arquivos que deixaram de ser usados.

Só reprocessa quando chega um arquivo novo (ainda não salvo no storage), então editar a
legenda de uma foto não mexe na imagem.
"""

from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.db import transaction
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


# Limpeza da pasta media: o Django não apaga o arquivo antigo quando uma foto é trocada,
# removida ("Limpar" no admin) ou quando o registro é excluído. Os sinais ficam em signals.py.
CAMPOS_DE_ARQUIVO = {
    "Snif": ["foto_capa"],
    "FotoSnif": ["imagem", "miniatura"],
    "Bagrut": ["foto"],
}


def _campos(instancia):
    return CAMPOS_DE_ARQUIVO.get(type(instancia).__name__, [])


def _apagar_depois_do_commit(campo, nome):
    """Apaga só quando a transação der certo (se o save falhar, o arquivo ainda é usado)."""
    storage = campo.storage
    transaction.on_commit(lambda: storage.delete(nome) if storage.exists(nome) else None)


def lembrar_arquivos_atuais(instancia):
    """Antes do save: guarda os nomes dos arquivos que estão no banco."""
    if not instancia.pk:
        instancia._arquivos_anteriores = {}
        return
    anterior = type(instancia).objects.filter(pk=instancia.pk).values(*_campos(instancia)).first()
    instancia._arquivos_anteriores = anterior or {}


def apagar_arquivos_substituidos(instancia):
    """Depois do save: apaga os arquivos que foram trocados ou removidos."""
    for nome_campo, nome_antigo in getattr(instancia, "_arquivos_anteriores", {}).items():
        campo = getattr(instancia, nome_campo)
        if nome_antigo and nome_antigo != campo.name:
            _apagar_depois_do_commit(campo, nome_antigo)


def apagar_arquivos(instancia):
    """Depois de excluir o registro (inclusive em cascata, ao excluir o snif)."""
    for nome_campo in _campos(instancia):
        campo = getattr(instancia, nome_campo)
        if campo.name:
            _apagar_depois_do_commit(campo, campo.name)
