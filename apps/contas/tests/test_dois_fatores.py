import pytest
from django.conf import settings
from django.urls import reverse
from django_otp.oath import totp
from django_otp.plugins.otp_static.models import StaticToken
from django_otp.plugins.otp_totp.models import TOTPDevice

from apps.contas import dois_fatores
from apps.contas.models import User

ADMIN = f"/{settings.ADMIN_URL}"
SENHA = "uma-senha-bem-forte-42"


def _codigo(device):
    return f"{totp(device.bin_key, step=device.step, digits=device.digits):06d}"


@pytest.fixture
def staff():
    return User.objects.create_superuser(email="admin@exemplo.com", password=SENHA)


@pytest.fixture
def com_2fa(staff):
    device = TOTPDevice.objects.create(user=staff, name="app", confirmed=True)
    codigos = dois_fatores.gerar_codigos_de_recuperacao(staff)
    return device, codigos


def _login_com_senha(client):
    return client.post(
        f"{ADMIN}login/", {"username": "admin@exemplo.com", "password": SENHA, "next": ADMIN}
    )


@pytest.mark.django_db
def test_so_a_senha_nao_abre_o_painel(client, staff, com_2fa):
    _login_com_senha(client)
    resposta = client.get(ADMIN, follow=True)
    assert resposta.redirect_chain[-1][0].startswith(reverse("contas:verificar_2fa"))
    assert client.get(f"{ADMIN}contas/user/").status_code == 302


@pytest.mark.django_db
def test_codigo_do_app_abre_o_painel(client, staff, com_2fa):
    device, _ = com_2fa
    _login_com_senha(client)
    client.post(reverse("contas:verificar_2fa"), {"codigo": _codigo(device), "next": ADMIN})
    assert client.get(ADMIN).status_code == 200


@pytest.mark.django_db
def test_codigo_errado_nao_abre(client, staff, com_2fa):
    _login_com_senha(client)
    resposta = client.post(reverse("contas:verificar_2fa"), {"codigo": "000000", "next": ADMIN})
    assert "Código inválido" in resposta.content.decode()
    assert client.get(ADMIN).status_code == 302


@pytest.mark.django_db
def test_erros_seguidos_bloqueiam_ate_o_codigo_certo(client, staff, com_2fa):
    """O django-otp aumenta a espera a cada erro: adivinhar 6 dígitos fica inviável."""
    device, _ = com_2fa
    _login_com_senha(client)
    for _ in range(3):
        client.post(reverse("contas:verificar_2fa"), {"codigo": "000000", "next": ADMIN})
    client.post(reverse("contas:verificar_2fa"), {"codigo": _codigo(device), "next": ADMIN})
    assert client.get(ADMIN).status_code == 302


@pytest.mark.django_db
def test_codigo_de_recuperacao_serve_uma_vez(client, staff, com_2fa):
    _, codigos = com_2fa
    _login_com_senha(client)
    client.post(reverse("contas:verificar_2fa"), {"codigo": codigos[0].upper(), "next": ADMIN})
    assert client.get(ADMIN).status_code == 200
    assert not StaticToken.objects.filter(token=codigos[0]).exists()


@pytest.mark.django_db
def test_primeiro_acesso_obriga_a_configurar(client, staff):
    _login_com_senha(client)
    resposta = client.get(ADMIN, follow=True)
    assert resposta.redirect_chain[-1][0].startswith(reverse("contas:configurar_2fa"))
    html = resposta.content.decode()
    assert "<svg" in html and "api.qrserver" not in html  # QR gerado aqui, sem terceiros


@pytest.mark.django_db
def test_configurar_ativa_o_app_e_mostra_codigos(client, staff):
    _login_com_senha(client)
    client.get(reverse("contas:configurar_2fa"))
    device = TOTPDevice.objects.get(user=staff, confirmed=False)
    resposta = client.post(
        reverse("contas:configurar_2fa"), {"codigo": _codigo(device), "next": ADMIN}
    )
    assert "Guarde estes códigos" in resposta.content.decode()
    device.refresh_from_db()
    assert device.confirmed
    assert StaticToken.objects.filter(device__user=staff).count() == dois_fatores.QUANTIDADE_CODIGOS
    assert client.get(ADMIN).status_code == 200


@pytest.mark.django_db
def test_senha_roubada_nao_cadastra_outro_celular(client, staff, com_2fa):
    """Quem já tem 2FA precisa passar por ele antes de trocar de aplicativo."""
    _login_com_senha(client)
    resposta = client.get(reverse("contas:configurar_2fa"))
    assert resposta.url.startswith(reverse("contas:verificar_2fa"))
    assert not TOTPDevice.objects.filter(user=staff, confirmed=False).exists()


@pytest.mark.django_db
def test_quem_nao_e_da_equipe_nao_usa_2fa(client):
    user = User.objects.create_user(email="pessoa@exemplo.com", password=SENHA)
    client.force_login(user)
    assert client.get(reverse("contas:configurar_2fa")).status_code == 403
    assert client.get(reverse("contas:verificar_2fa")).status_code == 403


@pytest.mark.django_db
def test_next_externo_e_ignorado(client, staff, com_2fa):
    device, _ = com_2fa
    _login_com_senha(client)
    resposta = client.post(
        reverse("contas:verificar_2fa"),
        {"codigo": _codigo(device), "next": "https://malicioso.com/"},
    )
    assert "malicioso" not in resposta.url


@pytest.mark.django_db
def test_sair_exige_2fa_de_novo(client, staff, com_2fa):
    device, _ = com_2fa
    _login_com_senha(client)
    client.post(reverse("contas:verificar_2fa"), {"codigo": _codigo(device), "next": ADMIN})
    client.post(reverse("contas:sair"))
    _login_com_senha(client)
    assert client.get(ADMIN).status_code == 302
