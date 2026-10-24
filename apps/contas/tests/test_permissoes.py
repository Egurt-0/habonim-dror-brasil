import pytest
from django.conf import settings
from django.contrib.auth.models import Group

from apps.contas.models import User
from apps.contas.permissoes import EDITOR_NACIONAL, EDITOR_SNIF, garantir_grupos
from apps.core.models import BlocoTexto
from apps.snifim.models import Bagrut, Snif

ADMIN = f"/{settings.ADMIN_URL}"


def _editor(grupo, *snifim, email="editor@exemplo.com"):
    user = User.objects.create_user(email=email, password="x", is_staff=True)
    user.groups.add(Group.objects.get(name=grupo))
    user.snifim.add(*snifim)
    return user


@pytest.fixture
def recife():
    return Snif.objects.get(slug="recife")


@pytest.fixture
def poa():
    return Snif.objects.get(slug="porto-alegre")


def _dados_do_form(snif, **mudancas):
    """POST mínimo do formulário do snif no admin (com os inlines vazios)."""
    dados = {
        "nome": snif.nome,
        "slug": snif.slug,
        "cidade": snif.cidade,
        "estado": snif.estado,
        "ano_fundacao": snif.ano_fundacao,
        "ativo": "on",
        "resumo": snif.resumo,
        "historia": snif.historia,
        "foto_capa_alt": "",
        "instagram": snif.instagram,
        "contato": "",
        "endereco": "",
        "kehila": snif.kehila_id or "",
        "cchd_descricao": "",
    }
    for prefixo in ["bagrutot", "fotos"]:
        dados.update(
            {
                f"{prefixo}-TOTAL_FORMS": "0",
                f"{prefixo}-INITIAL_FORMS": "0",
                f"{prefixo}-MIN_NUM_FORMS": "0",
                f"{prefixo}-MAX_NUM_FORMS": "1000",
            }
        )
    dados.update(mudancas)
    return dados


@pytest.mark.django_db
def test_grupos_existem_depois_do_migrate():
    assert Group.objects.filter(name__in=[EDITOR_NACIONAL, EDITOR_SNIF]).count() == 2


@pytest.mark.django_db
def test_garantir_grupos_desfaz_permissao_dada_a_mao():
    grupo = Group.objects.get(name=EDITOR_SNIF)
    from django.contrib.auth.models import Permission

    grupo.permissions.add(Permission.objects.get(codename="change_user"))
    garantir_grupos()
    assert not grupo.permissions.filter(codename="change_user").exists()


@pytest.mark.django_db
def test_editor_de_snif_so_ve_o_proprio_snif(painel, recife, poa):
    client = painel(_editor(EDITOR_SNIF, recife))
    html = client.get(f"{ADMIN}snifim/snif/").content.decode()
    assert f"/snifim/snif/{recife.pk}/change/" in html
    assert f"/snifim/snif/{poa.pk}/change/" not in html


@pytest.mark.django_db
def test_editor_de_snif_nao_abre_outro_snif_nem_por_link_direto(painel, recife, poa):
    client = painel(_editor(EDITOR_SNIF, recife))
    resposta = client.get(f"{ADMIN}snifim/snif/{poa.pk}/change/")
    assert resposta.status_code == 302  # o admin trata como "não encontrado"
    client.post(f"{ADMIN}snifim/snif/{poa.pk}/change/", _dados_do_form(poa, historia="invadido"))
    poa.refresh_from_db()
    assert poa.historia != "invadido"


@pytest.mark.django_db
def test_editor_de_snif_edita_o_texto_mas_nao_a_identidade(painel, recife):
    client = painel(_editor(EDITOR_SNIF, recife))
    dados = _dados_do_form(recife, historia="Nossa história.", nome="Hackeado", ativo="")
    resposta = client.post(f"{ADMIN}snifim/snif/{recife.pk}/change/", dados)
    assert resposta.status_code == 302
    recife.refresh_from_db()
    assert recife.historia == "Nossa história."
    assert recife.nome == "Recife" and recife.ativo


@pytest.mark.django_db
def test_editor_de_snif_nao_cria_nem_apaga_snif(painel, recife):
    client = painel(_editor(EDITOR_SNIF, recife))
    assert client.get(f"{ADMIN}snifim/snif/add/").status_code == 403
    assert client.get(f"{ADMIN}snifim/snif/{recife.pk}/delete/").status_code == 403


@pytest.mark.django_db
def test_editor_de_snif_cria_bagrut_do_proprio_snif(painel, recife):
    client = painel(_editor(EDITOR_SNIF, recife))
    dados = _dados_do_form(
        recife,
        **{
            "bagrutot-TOTAL_FORMS": "1",
            "bagrutot-0-gestao": "2026",
            "bagrutot-0-atual": "on",
            "bagrutot-0-descricao": "",
            "bagrutot-0-foto_alt": "",
        },
    )
    client.post(f"{ADMIN}snifim/snif/{recife.pk}/change/", dados)
    assert Bagrut.objects.filter(snif=recife, gestao="2026", atual=True).exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    ["core/blocotexto/", "contas/user/", "auth/group/", "snifim/kehila/", "glossario/termo/"],
)
def test_editor_de_snif_nao_ve_o_resto_do_painel(painel, recife, url):
    client = painel(_editor(EDITOR_SNIF, recife))
    assert client.get(f"{ADMIN}{url}").status_code == 403


@pytest.mark.django_db
def test_editor_nacional_edita_conteudo_e_todos_os_snifim(painel, recife, poa):
    client = painel(_editor(EDITOR_NACIONAL))
    assert client.get(f"{ADMIN}core/blocotexto/").status_code == 200
    html = client.get(f"{ADMIN}snifim/snif/").content.decode()
    assert f"/snifim/snif/{recife.pk}/change/" in html and f"/snifim/snif/{poa.pk}/change/" in html


@pytest.mark.django_db
@pytest.mark.parametrize("url", ["contas/user/", "auth/group/"])
def test_editor_nacional_nao_mexe_em_usuarios_nem_grupos(painel, url):
    client = painel(_editor(EDITOR_NACIONAL))
    assert client.get(f"{ADMIN}{url}").status_code == 403


@pytest.mark.django_db
def test_editor_nacional_nao_se_promove_a_superusuario(painel):
    editor = _editor(EDITOR_NACIONAL)
    client = painel(editor)
    client.post(f"{ADMIN}contas/user/{editor.pk}/change/", {"is_superuser": "on"})
    editor.refresh_from_db()
    assert not editor.is_superuser


@pytest.mark.django_db
def test_staff_sem_grupo_nao_edita_nada(painel, recife):
    user = User.objects.create_user(email="staff@exemplo.com", password="x", is_staff=True)
    client = painel(user)
    assert client.get(f"{ADMIN}snifim/snif/").status_code == 403
    assert client.get(f"{ADMIN}core/blocotexto/").status_code == 403


@pytest.mark.django_db
def test_nao_staff_nao_entra_no_painel(painel, recife):
    user = _editor(EDITOR_SNIF, recife)
    user.is_staff = False
    user.save()
    client = painel(user)
    assert client.get(f"{ADMIN}snifim/snif/").status_code == 302


@pytest.mark.django_db
def test_blocotexto_continua_protegido_para_anonimo(client):
    assert client.get(f"{ADMIN}core/blocotexto/").status_code == 302
    assert BlocoTexto.objects.exists()
