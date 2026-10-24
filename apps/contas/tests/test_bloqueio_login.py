import pytest
from django.conf import settings
from django.test import RequestFactory
from django.urls import reverse

from apps.contas.models import User
from apps.contas.services import ip_do_cliente
from config.settings.seguranca import chave_secreta_fraca

EMAIL = "madrich@exemplo.com"
SENHA = "senha-forte-123"


@pytest.fixture
def usuario():
    return User.objects.create_user(email=EMAIL, password=SENHA)


def _entrar(client, senha, ip="10.0.0.1"):
    return client.post(
        reverse("contas:entrar"), {"username": EMAIL, "password": senha}, REMOTE_ADDR=ip
    )


@pytest.mark.django_db
def test_bloqueia_depois_de_varias_senhas_erradas(client, usuario):
    for _ in range(settings.AXES_FAILURE_LIMIT):
        _entrar(client, "errada")
    resposta = _entrar(client, SENHA)  # nem a senha certa entra durante o bloqueio
    assert resposta.status_code == 429
    assert "Acesso bloqueado" in resposta.content.decode()
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_bloqueio_nao_afeta_a_pessoa_em_outro_ip(client, usuario):
    for _ in range(settings.AXES_FAILURE_LIMIT):
        _entrar(client, "errada", ip="10.0.0.1")
    resposta = _entrar(client, SENHA, ip="10.0.0.2")
    assert resposta.status_code == 302


@pytest.mark.django_db
def test_login_certo_zera_as_tentativas(client, usuario):
    for _ in range(settings.AXES_FAILURE_LIMIT - 1):
        _entrar(client, "errada")
    assert _entrar(client, SENHA).status_code == 302
    client.logout()
    _entrar(client, "errada")
    assert _entrar(client, SENHA).status_code == 302


@pytest.mark.django_db
def test_admin_tambem_e_protegido(client):
    User.objects.create_superuser(email=EMAIL, password=SENHA)
    url = f"/{settings.ADMIN_URL}login/"
    for _ in range(settings.AXES_FAILURE_LIMIT):
        client.post(url, {"username": EMAIL, "password": "errada"})
    assert client.post(url, {"username": EMAIL, "password": SENHA}).status_code == 429


def test_ip_sem_proxy_usa_remote_addr(settings):
    settings.ATRAS_DE_PROXY = False
    request = RequestFactory().get("/", REMOTE_ADDR="10.0.0.1", HTTP_X_FORWARDED_FOR="1.2.3.4")
    assert ip_do_cliente(request) == "10.0.0.1"


def test_ip_atras_de_proxy_usa_o_ip_que_o_proxy_acrescentou(settings):
    settings.ATRAS_DE_PROXY = True
    # "6.6.6.6" foi enviado pelo visitante (falsificável); "200.1.1.1" foi acrescentado pelo proxy.
    request = RequestFactory().get(
        "/", REMOTE_ADDR="127.0.0.1", HTTP_X_FORWARDED_FOR="6.6.6.6, 200.1.1.1"
    )
    assert ip_do_cliente(request) == "200.1.1.1"


@pytest.mark.parametrize(
    "chave",
    ["troque-por-uma-chave-longa-e-aleatoria", "django-insecure-" + "x" * 50, "curta", "a" * 60],
)
def test_chave_secreta_fraca_e_recusada(chave):
    assert chave_secreta_fraca(chave)


def test_chave_secreta_gerada_pelo_django_e_aceita():
    from django.core.management.utils import get_random_secret_key

    assert not chave_secreta_fraca(get_random_secret_key())
