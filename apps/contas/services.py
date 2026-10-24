"""Regras de conta: entrada com ou sem login, cadastro, e-mails e bloqueio de tentativas."""

from datetime import timedelta

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.cache import cache
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import User

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


# E-mails -----------------------------------------------------------------------------------

# Anti-abuso: no máximo N e-mails por endereço por hora (cadastro e "esqueci a senha"), para
# ninguém usar o site para encher a caixa de outra pessoa.
LIMITE_EMAILS_POR_HORA = 3


def pode_enviar_email(email):
    chave = f"contas:emails:{email.lower()}"
    cache.add(chave, 0, timeout=60 * 60)
    try:
        return cache.incr(chave) <= LIMITE_EMAILS_POR_HORA
    except ValueError:  # a chave expirou entre o add e o incr
        return True


def link_absoluto(nome_url, uidb64, token):
    """Link para e-mail montado com SITE_URL, nunca com o Host da requisição (forjável)."""
    return settings.SITE_URL + reverse(nome_url, args=[uidb64, token])


def enviar_email(para, assunto, template, contexto):
    corpo = render_to_string(template, {"site_url": settings.SITE_URL, **contexto})
    send_mail(assunto, corpo, None, [para])


# Cadastro ----------------------------------------------------------------------------------


class GeradorDeAtivacao(PasswordResetTokenGenerator):
    """Link de ativação de uso único: deixa de valer quando a conta é ativada ou ganha senha."""

    key_salt = "apps.contas.ativacao"

    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{user.is_active}{user.password}{user.email}{timestamp}"


gerador_de_ativacao = GeradorDeAtivacao()


def _enviar_ativacao(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    enviar_email(
        user.email,
        "Confirme seu cadastro no Habonim Dror Brasil",
        "contas/emails/ativacao.txt",
        {
            "user": user,
            "link": link_absoluto("contas:ativar", uid, gerador_de_ativacao.make_token(user)),
        },
    )


def cadastrar(first_name, email):
    """Cria a conta inativa e sem senha e manda o link para a pessoa criar a senha.

    A senha só é definida por quem abre o link, então ninguém consegue cadastrar o e-mail de
    outra pessoa com uma senha que conhece. A resposta na tela é sempre a mesma ("veja seu
    e-mail"), exista ou não uma conta, para o formulário não revelar quem tem cadastro.
    """
    email = User.objects.normalize_email(email)
    if not pode_enviar_email(email):
        return
    existente = User.objects.filter(email__iexact=email).first()
    if existente is None:
        agora = timezone.now()
        user = User.objects.create_user(
            email=email,
            password=None,  # senha inutilizável até a pessoa criar a dela pelo link
            first_name=first_name,
            is_active=False,
            aceitou_privacidade_em=agora,
            declarou_maioridade_em=agora,
        )
        _enviar_ativacao(user)
    elif not existente.is_active:
        _enviar_ativacao(existente)  # cadastro pendente: reenvia o link sem mudar a conta
    else:
        enviar_email(
            existente.email,
            "Você já tem conta no Habonim Dror Brasil",
            "contas/emails/conta_existente.txt",
            {"user": existente, "link": settings.SITE_URL + reverse("contas:esqueci_senha")},
        )
