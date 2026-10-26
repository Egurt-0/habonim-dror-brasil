import json
import re

import pytest
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse

PAGINAS = ["/", "/bases/", "/snifim/", "/snifim/recife/", "/glossario/", "/quero-saber-mais/"]


@pytest.mark.django_db
@pytest.mark.parametrize("url", PAGINAS)
def test_paginas_tem_canonical_e_previa_de_link(client, url):
    html = client.get(url).content.decode()
    assert f'<link rel="canonical" href="{settings.SITE_URL}{url}">' in html
    for propriedade in ["og:title", "og:description", "og:url", "og:image"]:
        assert f'property="{propriedade}"' in html
    assert f'property="og:image" content="{settings.SITE_URL}/static/' in html


@pytest.mark.django_db
def test_titulo_e_descricao_da_pagina_vao_para_a_previa(client):
    html = client.get("/snifim/recife/").content.decode()
    titulo = re.search(r"<title>(.*?)</title>", html).group(1)
    assert titulo == "Recife · Habonim Dror Brasil"
    assert f'<meta property="og:title" content="{titulo}">' in html
    assert html.count("<title>") == 1


@pytest.mark.django_db
def test_links_absolutos_nao_usam_o_host_da_requisicao(client):
    html = client.get("/", HTTP_HOST="atacante.example").content.decode()
    assert "atacante.example" not in html


@pytest.mark.django_db
def test_sitemap_lista_paginas_e_snifim_ativos(client):
    from apps.snifim.models import Snif

    Snif.objects.filter(slug="manaus").update(ativo=False)
    resposta = client.get(reverse("core:sitemap"))
    assert resposta["Content-Type"] == "application/xml"
    xml = resposta.content.decode()
    assert f"<loc>{settings.SITE_URL}/bases/</loc>" in xml
    assert f"<loc>{settings.SITE_URL}/snifim/recife/</loc>" in xml
    assert "/snifim/manaus/" not in xml
    assert "/contas/" not in xml


@pytest.mark.django_db
def test_robots_bloqueia_contas_e_nao_revela_o_admin(client):
    txt = client.get(reverse("core:robots")).content.decode()
    assert "Disallow: /contas/" in txt
    assert f"Sitemap: {settings.SITE_URL}/sitemap.xml" in txt
    assert settings.ADMIN_URL not in txt


@pytest.mark.django_db
def test_home_tem_dados_estruturados_validos(client):
    html = client.get("/").content.decode()
    bloco = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1)
    dados = json.loads(bloco)
    assert dados["@type"] == "Organization"
    assert dados["foundingDate"] == "1945"


@pytest.mark.django_db
def test_pagina_404_tem_a_cara_do_site(client):
    resposta = client.get("/nao-existe/")
    assert resposta.status_code == 404
    html = resposta.content.decode()
    assert "Página não encontrada" in html
    assert reverse("snifim:saber_mais") in html


def test_pagina_500_nao_depende_de_contexto():
    html = render_to_string("500.html")
    assert "Algo deu errado" in html
    assert 'href="/"' in html
