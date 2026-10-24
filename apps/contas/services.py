"""Escolha de entrada (com ou sem login) e o IP usado no bloqueio de tentativas de login."""

from datetime import timedelta

from django.conf import settings
from django.utils import timezone

SESSION_KEY_SEM_LOGIN = "seguir_sem_login"


def escolher_seguir_sem_login(request):
    request.session[SESSION_KEY_SEM_LOGIN] = True


def ja_escolheu_entrada(request):
    """True se o visitante está logado ou já escolheu seguir sem login."""
    return request.user.is_authenticated or request.session.get(SESSION_KEY_SEM_LOGIN, False)


def ip_do_cliente(request):
    """IP do visitante para o django-axes.

    Atrás de um proxy, REMOTE_ADDR é o IP do próprio proxy (igual para todo mundo). Nesse caso
    usa o último IP de X-Forwarded-For, que é o que o proxy acrescentou. Os anteriores vêm do
    visitante e podem ser falsificados, por isso não são usados.
    """
    if settings.ATRAS_DE_PROXY:
        encaminhado = request.META.get("HTTP_X_FORWARDED_FOR", "")
        ultimo = encaminhado.split(",")[-1].strip()
        if ultimo:
            return ultimo
    return request.META.get("REMOTE_ADDR")


# LGPD: registros de segurança (e-mail digitado, IP, navegador) só ficam pelo tempo necessário.
# O prazo aparece na política de privacidade (bloco priv_retencao); mudar lá também.
RETENCAO_REGISTROS_DIAS = 90


def apagar_registros_de_acesso_antigos(dias=RETENCAO_REGISTROS_DIAS):
    """Apaga tentativas e registros de login do django-axes mais velhos que `dias`.

    Devolve quantos registros foram apagados.
    """
    from axes.models import AccessAttempt, AccessFailureLog, AccessLog

    limite = timezone.now() - timedelta(days=dias)
    total = 0
    for model in (AccessAttempt, AccessFailureLog, AccessLog):
        apagados, _ = model.objects.filter(attempt_time__lt=limite).delete()
        total += apagados
    return total
