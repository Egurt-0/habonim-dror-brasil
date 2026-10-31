import re

import pytest
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.db import IntegrityError
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.contas.models import User
from apps.contas.services import LIMITE_EMAILS_POR_HORA

SENHA = "uma-senha-bem-forte-42"
DADOS = {
    "first_name": "Rivka",
    "email": "rivka@exemplo.com",
    "maior_de_idade": "on",
    "aceite": "on",
}


@pytest.fixture
def aberto(settings):
    settings.CADASTRO_ABERTO = True
    settings.SITE_URL = "https://site.exemplo.org.br"


def _link(email_msg):
    return re.search(r"https://site\.exemplo\.org\.br(/\S+)", email_msg.body).group(1)


def _cadastrar(client, **extra):
    return client.post(reverse("contas:cadastro"), {**DADOS, **extra})


def _criar_senha(client, link, senha=SENHA):
    """O Django troca o token da URL por um guardado na sessão antes de mostrar o formulário."""
    pagina = client.get(link, follow=True)
    url_form = pagina.redirect_chain[-1][0]
    return client.post(url_form, {"new_password1": senha, "new_password2": senha})


@pytest.mark.django_db
def test_cadastro_fechado_nao_cria_conta(client, settings):
    settings.CADASTRO_ABERTO = False
    resposta = _cadastrar(client)
    assert "abre em breve" in resposta.content.decode()
    assert not User.objects.exists()


@pytest.mark.django_db
def test_cadastro_cria_conta_inativa_sem_senha_e_manda_link(client, aberto):
    resposta = _cadastrar(client)
    assert resposta.url == reverse("contas:cadastro_enviado")
    user = User.objects.get()
    assert not user.is_active
    assert not user.has_usable_password()
    assert user.aceitou_privacidade_em and user.declarou_maioridade_em
    assert len(mail.outbox) == 1 and mail.outbox[0].to == ["rivka@exemplo.com"]


@pytest.mark.django_db
def test_fluxo_completo_ativa_a_conta_e_permite_login(client, aberto):
    _cadastrar(client)
    link = _link(mail.outbox[0])
    _criar_senha(client, link)
    user = User.objects.get()
    assert user.is_active and user.check_password(SENHA)
    entrar = client.post(
        reverse("contas:entrar"), {"username": "RIVKA@exemplo.com", "password": SENHA}
    )
    assert entrar.status_code == 302  # e-mail sem diferenciar maiúsculas
    client.logout()
    assert "não vale mais" in client.get(link, follow=True).content.decode()  # uso único


@pytest.mark.django_db
@pytest.mark.parametrize("faltando", ["maior_de_idade", "aceite", "email", "first_name"])
def test_cadastro_exige_maioridade_aceite_e_dados(client, aberto, faltando):
    dados = {k: v for k, v in DADOS.items() if k != faltando}
    resposta = client.post(reverse("contas:cadastro"), dados)
    assert resposta.status_code == 200
    assert not User.objects.exists()


@pytest.mark.django_db
def test_campos_extras_sao_ignorados(client, aberto):
    _cadastrar(client, is_staff="True", is_superuser="True", is_active="True", password="x")
    user = User.objects.get()
    assert not user.is_staff and not user.is_superuser and not user.is_active
    assert not user.has_usable_password()


@pytest.mark.django_db
def test_nao_revela_quem_ja_tem_conta(client, aberto):
    User.objects.create_user(email="rivka@exemplo.com", password=SENHA, first_name="Rivka")
    resposta = _cadastrar(client, email="Rivka@Exemplo.com")
    assert resposta.url == reverse("contas:cadastro_enviado")  # mesma resposta de sempre
    assert User.objects.count() == 1
    assert "já tem uma" in mail.outbox[0].body
    assert User.objects.get().check_password(SENHA)  # a conta existente não muda


@pytest.mark.django_db
def test_cadastro_pendente_reenvia_link_sem_mudar_a_conta(client, aberto):
    _cadastrar(client)
    _cadastrar(client, first_name="Outro nome")
    assert User.objects.get().first_name == "Rivka"
    assert len(mail.outbox) == 2


@pytest.mark.django_db
def test_conta_desativada_com_senha_nao_e_reativada_pelo_cadastro(client, aberto):
    desativada = User.objects.create_user(
        email="rivka@exemplo.com", password=SENHA, first_name="Rivka", is_staff=True
    )
    desativada.is_active = False
    desativada.save()

    resposta = _cadastrar(client)

    assert resposta.url == reverse("contas:cadastro_enviado")  # mesma resposta de sempre
    desativada.refresh_from_db()
    assert not desativada.is_active
    assert desativada.check_password(SENHA)
    assert "já tem uma" in mail.outbox[0].body  # recebe o aviso padrão, não um link de ativação


@pytest.mark.django_db
def test_limite_de_emails_por_endereco(client, aberto):
    for _ in range(LIMITE_EMAILS_POR_HORA + 2):
        _cadastrar(client)
    assert len(mail.outbox) == LIMITE_EMAILS_POR_HORA


@pytest.mark.django_db
def test_token_de_nova_senha_nao_serve_para_ativar_conta(client, aberto):
    _cadastrar(client)
    user = User.objects.get()
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    pagina = client.get(reverse("contas:ativar", args=[uid, token]), follow=True)
    assert "não vale mais" in pagina.content.decode()


@pytest.mark.django_db
def test_link_do_email_usa_site_url_e_nao_o_host_da_requisicao(client, aberto, settings):
    settings.ALLOWED_HOSTS = ["*"]
    client.post(reverse("contas:cadastro"), DADOS, HTTP_HOST="malicioso.com")
    assert "malicioso.com" not in mail.outbox[0].body
    assert "https://site.exemplo.org.br/contas/ativar/" in mail.outbox[0].body


@pytest.mark.django_db
def test_esqueci_senha_manda_link_so_para_conta_ativa(client, aberto):
    User.objects.create_user(email="ativa@exemplo.com", password=SENHA)
    User.objects.create_user(email="inativa@exemplo.com", password=SENHA, is_active=False)
    for email in ["ativa@exemplo.com", "inativa@exemplo.com", "ninguem@exemplo.com"]:
        resposta = client.post(reverse("contas:esqueci_senha"), {"email": email})
        assert resposta.url == reverse("contas:esqueci_senha_enviado")  # sempre igual
    assert [m.to for m in mail.outbox] == [["ativa@exemplo.com"]]


@pytest.mark.django_db
def test_redefinir_senha_pelo_link(client, aberto):
    user = User.objects.create_user(email="ativa@exemplo.com", password="antiga-senha-123")
    client.post(reverse("contas:esqueci_senha"), {"email": "ativa@exemplo.com"})
    _criar_senha(client, _link(mail.outbox[0]))
    user.refresh_from_db()
    assert user.check_password(SENHA)


@pytest.mark.django_db
def test_email_unico_sem_diferenciar_maiusculas():
    User.objects.create_user(email="pessoa@exemplo.com", password=SENHA)
    with pytest.raises(IntegrityError):
        User.objects.create_user(email="PESSOA@exemplo.com", password=SENHA)
