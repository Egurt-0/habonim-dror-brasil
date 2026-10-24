from io import BytesIO
from pathlib import Path

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from apps.snifim.models import Bagrut, FotoSnif, Snif


@pytest.fixture(autouse=True)
def _media_temporaria(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path


@pytest.fixture
def no_commit(django_capture_on_commit_callbacks):
    """Roda os on_commit na hora (no teste a transação nunca chega a ser confirmada)."""
    return lambda: django_capture_on_commit_callbacks(execute=True)


def _foto(nome="foto.jpg"):
    saida = BytesIO()
    Image.new("RGB", (800, 600), "red").save(saida, "JPEG")
    return SimpleUploadedFile(nome, saida.getvalue(), content_type="image/jpeg")


@pytest.fixture
def recife():
    return Snif.objects.get(slug="recife")


@pytest.mark.django_db
def test_trocar_foto_de_capa_apaga_a_antiga(recife, no_commit):
    recife.foto_capa = _foto("a.jpg")
    recife.save()
    antiga = Path(recife.foto_capa.path)
    with no_commit():
        recife.foto_capa = _foto("b.jpg")
        recife.save()
    assert not antiga.exists()
    assert Path(recife.foto_capa.path).exists()


@pytest.mark.django_db
def test_limpar_foto_apaga_o_arquivo(recife, no_commit):
    bagrut = Bagrut.objects.create(snif=recife, gestao="2026", foto=_foto())
    arquivo = Path(bagrut.foto.path)
    with no_commit():
        bagrut.foto = None
        bagrut.save()
    assert not arquivo.exists()


@pytest.mark.django_db
def test_editar_legenda_nao_apaga_nada(recife, no_commit):
    foto = FotoSnif.objects.create(snif=recife, imagem=_foto(), alt="roda")
    with no_commit():
        foto.legenda = "Machané 2026"
        foto.save()
    assert Path(foto.imagem.path).exists()
    assert Path(foto.miniatura.path).exists()


@pytest.mark.django_db
def test_excluir_foto_apaga_imagem_e_miniatura(recife, no_commit):
    foto = FotoSnif.objects.create(snif=recife, imagem=_foto(), alt="roda")
    arquivos = [Path(foto.imagem.path), Path(foto.miniatura.path)]
    with no_commit():
        foto.delete()
    assert not any(a.exists() for a in arquivos)


@pytest.mark.django_db
def test_excluir_snif_apaga_as_fotos_em_cascata(recife, no_commit):
    foto = FotoSnif.objects.create(snif=recife, imagem=_foto(), alt="roda")
    bagrut = Bagrut.objects.create(snif=recife, gestao="2026", foto=_foto("bagrut.jpg"))
    arquivos = [Path(foto.imagem.path), Path(foto.miniatura.path), Path(bagrut.foto.path)]
    with no_commit():
        recife.delete()
    assert not any(a.exists() for a in arquivos)


@pytest.mark.django_db
def test_sem_commit_nada_e_apagado(recife):
    """Se a transação for desfeita, o arquivo antigo continua (o banco ainda aponta para ele)."""
    recife.foto_capa = _foto("a.jpg")
    recife.save()
    antiga = Path(recife.foto_capa.path)
    recife.foto_capa = _foto("b.jpg")
    recife.save()
    assert antiga.exists()
