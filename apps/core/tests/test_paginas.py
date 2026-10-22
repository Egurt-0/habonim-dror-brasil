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
def test_linha_do_tempo_na_pagina_bases(client):
    html = client.get(reverse("movimento:bases")).content.decode()
    assert "1945" in html and "2013" in html
