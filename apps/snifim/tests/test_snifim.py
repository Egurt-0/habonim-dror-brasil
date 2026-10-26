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
def test_todo_snif_vem_com_instagram(client):
    assert not Snif.objects.filter(instagram="").exists()
    html = client.get(reverse("snifim:detalhe", args=["bahia"])).content.decode()
    assert "https://www.instagram.com/drorzinhoba/" in html


@pytest.mark.django_db
def test_instagram_preenchido_vira_link(client):
    Snif.objects.filter(slug="recife").update(instagram="habonimrecife")
    html = client.get(reverse("snifim:saber_mais")).content.decode()
    assert "https://www.instagram.com/habonimrecife/" in html


@pytest.mark.django_db
@pytest.mark.parametrize("url", ["/snifim/", "/quero-saber-mais/", "/bases/"])
def test_curitiba_aparece_primeiro_nas_listas(client, url):
    html = client.get(url).content.decode()
    posicoes = {nome: html.find(f">{nome}") for nome in ["Curitiba", "Bahia", "Belo Horizonte"]}
    assert all(p >= 0 for p in posicoes.values()), posicoes
    assert posicoes["Curitiba"] < posicoes["Bahia"] < posicoes["Belo Horizonte"]


@pytest.mark.django_db
def test_demais_snifim_seguem_em_ordem_alfabetica():
    nomes = list(snifim_ativos().values_list("nome", flat=True))
    assert nomes[0] == "Curitiba"
    assert nomes[1:] == sorted(nomes[1:])


@pytest.fixture
def banner_curitiba(tmp_path, settings):
    """Pasta static/ temporária com img/snifim/curitiba.jpg."""
    (tmp_path / "img" / "snifim").mkdir(parents=True)
    (tmp_path / "img" / "snifim" / "curitiba.jpg").write_bytes(b"jpg")
    settings.STATICFILES_DIRS = [tmp_path]
    settings.DEBUG = True  # sem o cache de imagens.achar


@pytest.mark.django_db
def test_banner_do_snif_vem_de_static_pelo_slug(client, banner_curitiba):
    curitiba = Snif.objects.get(slug="curitiba")
    assert curitiba.capa_url == "/static/img/snifim/curitiba.jpg"
    assert Snif.objects.get(slug="recife").capa_url == ""

    pagina = client.get(curitiba.get_absolute_url()).content.decode()
    assert "background-image: url('/static/img/snifim/curitiba.jpg')" in pagina
    assert 'og:image" content="http://localhost:8000/static/img/snifim/curitiba.jpg"' in pagina

    lista = client.get(reverse("snifim:lista")).content.decode()
    assert "background-image: url('/static/img/snifim/curitiba.jpg')" in lista
    assert lista.count("topico--sem-foto") == 9
