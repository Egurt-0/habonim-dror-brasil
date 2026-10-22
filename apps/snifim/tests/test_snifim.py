import pytest
from django.urls import reverse

from apps.snifim.models import Snif
from apps.snifim.selectors import linha_do_tempo, snifim_ativos


@pytest.mark.django_db
def test_dez_snifim_carregados():
    assert snifim_ativos().count() == 10


@pytest.mark.django_db
def test_linha_do_tempo_agrupa_por_ano():
    linha = dict(linha_do_tempo())
    assert {s.nome for s in linha[1945]} == {"Curitiba", "Porto Alegre"}
    assert list(linha) == sorted(linha)


@pytest.mark.django_db
def test_snif_inativo_some_do_site(client):
    Snif.objects.filter(slug="manaus").update(ativo=False)
    html = client.get(reverse("snifim:saber_mais")).content.decode()
    assert "Manaus" not in html


@pytest.mark.django_db
def test_instagram_preenchido_vira_link(client):
    Snif.objects.filter(slug="recife").update(instagram="habonimrecife")
    html = client.get(reverse("snifim:saber_mais")).content.decode()
    assert "https://www.instagram.com/habonimrecife/" in html
