from datetime import timedelta

import pytest
from axes.models import AccessAttempt, AccessLog
from django.contrib.sessions.models import Session
from django.core.management import call_command
from django.urls import reverse
from django.utils import timezone

from apps.contas.models import User
from apps.contas.services import RETENCAO_CADASTROS_PENDENTES_DIAS, RETENCAO_REGISTROS_DIAS
from apps.core.models import BlocoTexto


@pytest.mark.django_db
def test_pagina_de_privacidade_mostra_as_secoes(client):
    html = client.get(reverse("core:privacidade")).content.decode()
    for chave in ["priv_dados", "priv_fotos", "priv_direitos", "priv_retencao"]:
        assert BlocoTexto.objects.get(chave=chave).titulo in html
    assert "será publicado em breve" in html  # encarregado ainda não preenchido
    assert "Última atualização" in html


@pytest.mark.django_db
def test_contato_do_encarregado_aparece_quando_preenchido(client):
    BlocoTexto.objects.filter(chave="priv_encarregado").update(texto="dpo@exemplo.org.br")
    html = client.get(reverse("core:privacidade")).content.decode()
    assert 'href="mailto:dpo@exemplo.org.br"' in html
    assert "será publicado em breve" not in html


@pytest.mark.django_db
def test_politica_cita_o_mesmo_prazo_de_retencao_do_codigo(client):
    assert f"{RETENCAO_REGISTROS_DIAS} dias" in BlocoTexto.objects.get(chave="priv_retencao").texto


@pytest.mark.django_db
@pytest.mark.parametrize("url", ["/", "/contas/entrar/"])
def test_link_para_a_privacidade(client, url):
    assert reverse("core:privacidade") in client.get(url).content.decode()


@pytest.mark.django_db
def test_site_nao_carrega_recursos_de_terceiros(client):
    """Sem fontes, scripts ou analytics de fora: o IP do visitante não vai para terceiros."""
    for url in ["/", "/bases/", "/snifim/recife/", "/privacidade/"]:
        html = client.get(url).content.decode()
        assert 'src="http' not in html
        assert '<link rel="stylesheet" href="http' not in html


def _registro(model, dias_atras, **campos):
    obj = model.objects.create(ip_address="10.0.0.1", user_agent="teste", **campos)
    model.objects.filter(pk=obj.pk).update(attempt_time=timezone.now() - timedelta(days=dias_atras))


@pytest.mark.django_db
def test_limpeza_apaga_registros_de_login_antigos_e_sessoes_expiradas():
    _registro(AccessAttempt, RETENCAO_REGISTROS_DIAS + 1, username="velho", failures_since_start=1)
    _registro(AccessAttempt, 1, username="recente", failures_since_start=1)
    _registro(AccessLog, RETENCAO_REGISTROS_DIAS + 1, username="velho")
    Session.objects.create(
        session_key="expirada", session_data="", expire_date=timezone.now() - timedelta(days=1)
    )

    call_command("limpar_dados_pessoais")

    assert list(AccessAttempt.objects.values_list("username", flat=True)) == ["recente"]
    assert not AccessLog.objects.exists()
    assert not Session.objects.filter(session_key="expirada").exists()


def _conta(email, dias_atras, is_active, senha=None):
    user = User.objects.create_user(email=email, password=senha, is_active=is_active)
    User.objects.filter(pk=user.pk).update(date_joined=timezone.now() - timedelta(days=dias_atras))
    return user


@pytest.mark.django_db
def test_limpeza_apaga_pendente_vencido_e_mantem_desativado_com_senha_e_pendente_recente():
    pendente_antigo = _conta(
        "pendente-antigo@exemplo.com", RETENCAO_CADASTROS_PENDENTES_DIAS + 1, is_active=False
    )
    desativado_com_senha = _conta(
        "desativado@exemplo.com",
        RETENCAO_CADASTROS_PENDENTES_DIAS + 1,
        is_active=False,
        senha="uma-senha-bem-forte-42",
    )
    pendente_recente = _conta("pendente-recente@exemplo.com", 1, is_active=False)

    call_command("limpar_dados_pessoais")

    restantes = set(User.objects.values_list("email", flat=True))
    assert pendente_antigo.email not in restantes
    assert desativado_com_senha.email in restantes
    assert pendente_recente.email in restantes
