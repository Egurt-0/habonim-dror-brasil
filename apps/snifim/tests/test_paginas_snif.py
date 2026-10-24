from io import BytesIO

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image

from apps.snifim.models import Bagrut, FotoSnif, Snif
from apps.snifim.services import LADO_MAXIMO, LADO_MINIATURA
from apps.snifim.validators import validar_imagem


@pytest.fixture(autouse=True)
def _media_temporaria(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path


def _foto(nome="foto.jpg", tamanho=(3000, 2000)):
    saida = BytesIO()
    Image.new("RGB", tamanho, "red").save(saida, "JPEG")
    return SimpleUploadedFile(nome, saida.getvalue(), content_type="image/jpeg")


@pytest.fixture
def recife():
    return Snif.objects.get(slug="recife")


@pytest.mark.django_db
def test_lista_mostra_todos_os_snifim_com_link(client):
    html = client.get(reverse("snifim:lista")).content.decode()
    for snif in Snif.objects.all():
        assert snif.get_absolute_url() in html


@pytest.mark.django_db
def test_pagina_do_snif_sem_conteudo_ainda_funciona(client, recife):
    resposta = client.get(reverse("snifim:detalhe", args=["recife"]))
    html = resposta.content.decode()
    assert resposta.status_code == 200
    assert "será publicada em breve" in html
    assert "Federação Israelita de Pernambuco" in html
    assert 'id="galeria"' not in html


@pytest.mark.django_db
def test_snif_inativo_da_404(client, recife):
    recife.ativo = False
    recife.save()
    assert client.get(reverse("snifim:detalhe", args=["recife"])).status_code == 404


@pytest.mark.django_db
def test_historia_passa_pelo_glossario(client, recife):
    recife.historia = "Os chanichim se encontram todo sábado."
    recife.save()
    html = client.get(recife.get_absolute_url()).content.decode()
    assert 'class="termo"' in html


@pytest.mark.django_db
def test_foto_da_galeria_e_reduzida_e_ganha_miniatura(recife):
    foto = FotoSnif.objects.create(snif=recife, imagem=_foto(), alt="chanichim", autorizada=True)
    with Image.open(foto.imagem.path) as img:
        assert max(img.size) == LADO_MAXIMO
    with Image.open(foto.miniatura.path) as img:
        assert max(img.size) == LADO_MINIATURA
    assert "snifim/recife/galeria/" in foto.imagem.name


@pytest.mark.django_db
def test_foto_sem_autorizacao_nao_aparece(client, recife):
    FotoSnif.objects.create(snif=recife, imagem=_foto("a.jpg"), alt="autorizada", autorizada=True)
    FotoSnif.objects.create(snif=recife, imagem=_foto("b.jpg"), alt="sem autorizacao")
    html = client.get(recife.get_absolute_url()).content.decode()
    assert 'alt="autorizada"' in html
    assert "sem autorizacao" not in html


@pytest.mark.django_db
def test_so_uma_bagrut_atual_por_snif(client, recife):
    antiga = Bagrut.objects.create(snif=recife, gestao="2025", atual=True)
    Bagrut.objects.create(snif=recife, gestao="2026", atual=True)
    antiga.refresh_from_db()
    assert not antiga.atual
    html = client.get(recife.get_absolute_url()).content.decode()
    assert "Bagrut 2026" in html
    assert "Bagrut 2025" not in html


@pytest.mark.django_db
def test_trocar_bagrut_atual_passa_na_validacao(recife):
    Bagrut.objects.create(snif=recife, gestao="2025", atual=True)
    nova = Bagrut(snif=recife, gestao="2026", atual=True)
    nova.full_clean()  # o admin chama full_clean antes de salvar


@pytest.mark.django_db
def test_foto_da_bagrut_sem_autorizacao_nao_aparece(client, recife):
    Bagrut.objects.create(
        snif=recife, gestao="2026", atual=True, foto=_foto(), foto_alt="Bagrut reunida"
    )
    html = client.get(recife.get_absolute_url()).content.decode()
    assert "Bagrut reunida" not in html


def test_rejeita_arquivo_que_nao_e_imagem():
    with pytest.raises(ValidationError):
        validar_imagem(SimpleUploadedFile("planilha.pdf", b"%PDF"))


def test_rejeita_foto_grande_demais():
    with pytest.raises(ValidationError):
        validar_imagem(SimpleUploadedFile("enorme.jpg", b"0" * (9 * 1024 * 1024)))


@pytest.mark.filterwarnings("ignore::PIL.Image.DecompressionBombWarning")
def test_rejeita_foto_com_dimensoes_enormes():
    """PNG de uma cor só: poucos KB, mas 10000×6000 pixels (60 MP) ao abrir."""
    saida = BytesIO()
    Image.new("1", (10_000, 6_000)).save(saida, "PNG")
    assert len(saida.getvalue()) < 1024 * 1024
    with pytest.raises(ValidationError, match="dimensões"):
        validar_imagem(SimpleUploadedFile("bomba.png", saida.getvalue()))


def test_rejeita_arquivo_com_extensao_de_imagem_que_nao_e_imagem():
    with pytest.raises(ValidationError, match="não é uma imagem"):
        validar_imagem(SimpleUploadedFile("falsa.jpg", b"<html>nao sou foto</html>"))


def test_aceita_foto_normal():
    validar_imagem(_foto())
