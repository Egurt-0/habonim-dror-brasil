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
def test_logos_oficiais_aparecem(client):
    html = client.get(reverse("core:home")).content.decode()
    assert 'class="marca__semel" src="/static/img/logos/semel.png"' in html
    assert '<link rel="icon" href="/static/img/logos/semel-circulo.png">' in html
    assert 'class="hero__semel" src="/static/img/logos/semel-branco.png"' in html
    assert 'class="chamada__logo" src="/static/img/logos/logo-completo.png"' in html


@pytest.mark.django_db
def test_sem_logos_o_site_continua_funcionando(client, monkeypatch):
    monkeypatch.setattr("apps.core.imagens.achar", lambda caminho: None)
    html = client.get(reverse("core:home")).content.decode()
    assert "marca__semel" not in html
    assert "Habonim Dror" in html


@pytest.mark.django_db
def test_topicos_da_home_com_saiba_mais(client):
    html = client.get(reverse("core:home")).content.decode()
    assert html.count("Saiba mais") >= 9
    assert 'href="/bases/#pilares"' in html
    assert 'href="/shichavot-bogrot/#shnat"' in html


@pytest.mark.django_db
def test_topico_sem_foto_fica_vermelho_e_com_foto_usa_imagem(client, monkeypatch):
    from apps.core import imagens

    original = imagens.achar
    monkeypatch.setattr(
        "apps.core.imagens.achar",
        lambda c: "img/topicos/pilares.jpg" if c == "img/topicos/pilares" else original(c),
    )
    html = client.get(reverse("core:home")).content.decode()
    assert "url('/static/img/topicos/pilares.jpg')" in html
    assert "topico--sem-foto" in html


@pytest.mark.django_db
def test_fotos_de_fundo_da_home(client, monkeypatch):
    fotos = ["img/fundos/a.jpg", "img/fundos/b.jpg"]
    monkeypatch.setattr("apps.core.views.fotos_de_fundo", lambda: fotos)
    html = client.get(reverse("core:home")).content.decode()
    assert html.count("url('/static/img/fundos/") == 2
    assert "hero--sem-foto" not in html


@pytest.mark.django_db
def test_cabecalho_da_pagina_usa_foto_quando_existe(client, monkeypatch):
    from apps.core import imagens

    original = imagens.achar
    monkeypatch.setattr(
        "apps.core.imagens.achar",
        lambda c: "img/paginas/bases.jpg" if c == "img/paginas/bases" else original(c),
    )
    html = client.get(reverse("movimento:bases")).content.decode()
    assert "url('/static/img/paginas/bases.jpg')" in html


@pytest.mark.django_db
def test_linha_do_tempo_na_pagina_bases(client):
    html = client.get(reverse("movimento:bases")).content.decode()
    assert "1945" in html and "2013" in html


@pytest.mark.django_db
def test_admin_nao_fica_em_barra_admin(client):
    from django.conf import settings

    assert settings.ADMIN_URL != "admin/"
    assert client.get("/admin/").status_code == 404
    assert client.get(f"/{settings.ADMIN_URL}").status_code == 302  # manda para o login


def test_idade_do_movimento_e_calculada_pelo_ano():
    from datetime import date

    from apps.core.movimento import anos_de_movimento, com_anos

    assert anos_de_movimento(date(2026, 10, 23)) == 81
    assert anos_de_movimento(date(2027, 1, 1)) == 82
    assert com_anos("sem marcador") == "sem marcador"
    assert com_anos("{anos} anos") == f"{anos_de_movimento()} anos"


@pytest.mark.django_db
def test_paginas_mostram_a_idade_atual_e_nao_o_marcador(client):
    from apps.core.movimento import anos_de_movimento

    anos = anos_de_movimento()
    for url in ["/", "/bases/"]:
        html = client.get(url).content.decode()
        assert "{anos}" not in html
        assert f"{anos} anos" in html


@pytest.mark.django_db
def test_shichavot_ficam_juntas_num_submenu(client):
    html = client.get("/shichavot-bogrot/").content.decode()
    topo = html.split('id="menu-principal"')[1].split("</nav>")[0]
    assert "menu__grupo menu__grupo--atual" in topo
    assert 'aria-controls="submenu-2"' in topo
    assert '<a href="/shichavot-tzeirot/">Tzeirot (ST)</a>' in topo
    assert '<a href="/shichavot-bogrot/" aria-current="page">Bogrot (SB)</a>' in topo
    rodape = html.split('aria-label="Rodapé"')[1]
    assert "Shichavot Tzeirot (ST)" in rodape and "Shichavot Bogrot (SB)" in rodape
