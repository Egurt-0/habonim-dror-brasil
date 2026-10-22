import pytest
from django.urls import reverse

from apps.core.models import BlocoTexto
from apps.core.selectors import blocos

PAGINAS = [
    ("core:home", "Habonim Dror Brasil"),
    ("movimento:bases", "Os quatro pilares"),
    ("movimento:st", "Sábados de atividade"),
    ("movimento:sb", "Magshimim"),
    ("movimento:kehila", "Vinho Guefen"),
    ("glossario:lista", "Núcleo local do movimento"),
    ("snifim:saber_mais", "Fortaleza"),
    ("contas:entrar", "Entrar"),
]


@pytest.mark.django_db
@pytest.mark.parametrize(("nome", "trecho"), PAGINAS)
def test_paginas_publicas_abrem_sem_login(client, nome, trecho):
    resposta = client.get(reverse(nome))
    assert resposta.status_code == 200
    assert trecho in resposta.content.decode()


@pytest.mark.django_db
def test_bloco_vazio_nao_aparece(client):
    # O Censo ainda não tem texto: a seção não deve aparecer.
    html = client.get(reverse("movimento:kehila")).content.decode()
    assert 'id="censo"' not in html


@pytest.mark.django_db
def test_bloco_editado_no_admin_aparece_no_site(client):
    BlocoTexto.objects.filter(chave="kh_censo").update(texto="Participe do Censo HDBR.")
    html = client.get(reverse("movimento:kehila")).content.decode()
    assert "Participe do Censo HDBR." in html


@pytest.mark.django_db
def test_bloco_inexistente_nao_quebra():
    bloco = blocos("nao_existe")["nao_existe"]
    assert bloco.texto == ""


@pytest.mark.django_db
def test_tochniot_sem_paragrafo_aninhado(client):
    html = client.get(reverse("movimento:sb")).content.decode()
    assert "<p><p>" not in html.replace("\n", "").replace(" ", "")


@pytest.mark.django_db
def test_rotulos_dos_numeros_tem_glossario(client):
    html = client.get(reverse("movimento:bases")).content.decode()
    assert '<span class="numero__rotulo"><a class="termo" href="/glossario/#chaver"' in html


@pytest.mark.django_db
def test_secao_vazia_em_bases_nao_deixa_titulo_vazio(client):
    BlocoTexto.objects.filter(chave__in=["quem_somos", "historia", "parceiros"]).delete()
    html = client.get(reverse("movimento:bases")).content.decode()
    assert "<h2></h2>" not in html
    assert 'href="#quem-somos"' not in html
    assert "<h2>História</h2>" in html


@pytest.mark.django_db
def test_contagem_de_snifim_vem_do_banco(client):
    from apps.snifim.models import Snif

    Snif.objects.filter(slug="manaus").update(ativo=False)
    html = client.get(reverse("movimento:bases")).content.decode()
    assert "Os 9 snifim" in html


@pytest.mark.django_db
def test_slogan_editado_aparece_no_rodape(client):
    BlocoTexto.objects.filter(chave="slogan").update(titulo="Slogan novo.")
    html = client.get(reverse("movimento:st")).content.decode()
    assert "Slogan novo." in html


@pytest.mark.django_db
def test_linha_do_tempo_na_pagina_bases(client):
    html = client.get(reverse("movimento:bases")).content.decode()
    assert "1945" in html and "2013" in html
