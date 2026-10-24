import json

import pytest
from axes.models import AccessAttempt
from django.urls import reverse

from apps.contas.models import User

SENHA = "uma-senha-bem-forte-42"


@pytest.fixture
def user():
    return User.objects.create_user(email="rivka@exemplo.com", password=SENHA, first_name="Rivka")


@pytest.fixture
def logado(client, user):
    client.force_login(user)
    return client


@pytest.mark.django_db
@pytest.mark.parametrize("nome", ["meus_dados", "baixar_dados", "excluir_conta", "trocar_senha"])
def test_paginas_de_conta_exigem_login(client, nome):
    resposta = client.get(reverse(f"contas:{nome}"))
    assert resposta.status_code == 302
    assert resposta.url.startswith(reverse("contas:entrar"))


@pytest.mark.django_db
def test_corrigir_nome_sem_mexer_em_outros_campos(logado, user):
    logado.post(
        reverse("contas:meus_dados"),
        {"first_name": "Rivka", "last_name": "Levi", "is_staff": "True", "email": "x@x.com"},
    )
    user.refresh_from_db()
    assert user.last_name == "Levi"
    assert not user.is_staff and user.email == "rivka@exemplo.com"


@pytest.mark.django_db
def test_baixar_meus_dados_inclui_conta_e_registros_de_login(logado, user):
    AccessAttempt.objects.create(
        username="rivka@exemplo.com",
        ip_address="10.0.0.1",
        user_agent="Firefox",
        failures_since_start=1,
    )
    AccessAttempt.objects.create(
        username="outra@exemplo.com",
        ip_address="10.0.0.9",
        user_agent="Outro",
        failures_since_start=1,
    )
    resposta = logado.get(reverse("contas:baixar_dados"))
    assert "attachment" in resposta["Content-Disposition"]
    dados = json.loads(resposta.content)
    assert dados["conta"]["email"] == "rivka@exemplo.com"
    ips = [r["ip"] for r in dados["registros_de_login"]]
    assert "10.0.0.1" in ips and "10.0.0.9" not in ips  # só os registros dela
    assert "password" not in json.dumps(dados) and SENHA not in json.dumps(dados)


@pytest.mark.django_db
def test_excluir_conta_exige_a_senha(logado, user):
    resposta = logado.post(reverse("contas:excluir_conta"), {"senha": "errada"})
    assert resposta.status_code == 200
    assert User.objects.filter(pk=user.pk).exists()


@pytest.mark.django_db
def test_excluir_conta_apaga_conta_e_registros_e_desloga(logado, user):
    AccessAttempt.objects.create(
        username="rivka@exemplo.com", ip_address="10.0.0.1", user_agent="x", failures_since_start=1
    )
    resposta = logado.post(reverse("contas:excluir_conta"), {"senha": SENHA})
    assert resposta.url == reverse("core:home")
    assert not User.objects.filter(pk=user.pk).exists()
    assert not AccessAttempt.objects.filter(username="rivka@exemplo.com").exists()
    assert "_auth_user_id" not in logado.session


@pytest.mark.django_db
def test_conta_do_painel_nao_se_exclui_pelo_site(client):
    staff = User.objects.create_user(email="staff@exemplo.com", password=SENHA, is_staff=True)
    client.force_login(staff)
    client.post(reverse("contas:excluir_conta"), {"senha": SENHA})
    assert User.objects.filter(pk=staff.pk).exists()


@pytest.mark.django_db
def test_excluir_conta_exige_csrf(user):
    from django.test import Client

    client = Client(enforce_csrf_checks=True)
    client.force_login(user)
    assert client.post(reverse("contas:excluir_conta"), {"senha": SENHA}).status_code == 403
    assert User.objects.filter(pk=user.pk).exists()


@pytest.mark.django_db
def test_trocar_senha_mantem_logado(logado, user):
    nova = "outra-senha-bem-forte-77"
    logado.post(
        reverse("contas:trocar_senha"),
        {"old_password": SENHA, "new_password1": nova, "new_password2": nova},
    )
    user.refresh_from_db()
    assert user.check_password(nova)
    assert logado.get(reverse("contas:meus_dados")).status_code == 200


@pytest.mark.django_db
def test_nome_no_cabecalho_leva_aos_meus_dados(logado):
    assert reverse("contas:meus_dados") in logado.get("/").content.decode()
