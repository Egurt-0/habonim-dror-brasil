"""Verificação em duas etapas (2FA) da equipe do painel, com django-otp.

- Aplicativo autenticador (TOTP: Google Authenticator, Authy, 2FAS...).
- 10 códigos de recuperação de uso único, para quem perder o celular.
- Tentativas erradas são freadas pelo próprio django-otp (espera cresce a cada erro).
- Para zerar o 2FA de quem perdeu celular e códigos: um superusuário apaga os dispositivos
  da pessoa no painel (OTP_TOTP / OTP_STATIC) e ela configura de novo no próximo login.
"""

import secrets

import qrcode
import qrcode.image.svg
from django_otp import devices_for_user, match_token
from django_otp.plugins.otp_static.models import StaticDevice, StaticToken
from django_otp.plugins.otp_totp.models import TOTPDevice

NOME_APP = "Aplicativo autenticador"
NOME_RECUPERACAO = "Códigos de recuperação"
QUANTIDADE_CODIGOS = 10


def tem_2fa(user):
    return any(devices_for_user(user, confirmed=True))


def dispositivo_em_configuracao(user):
    """TOTP ainda não confirmado (o QR mostrado na tela). Cria se não existir."""
    device = TOTPDevice.objects.filter(user=user, confirmed=False).first()
    return device or TOTPDevice.objects.create(user=user, name=NOME_APP, confirmed=False)


def qr_svg(device):
    """QR code em SVG gerado aqui mesmo (o segredo nunca vai para serviço de terceiros)."""
    imagem = qrcode.make(device.config_url, image_factory=qrcode.image.svg.SvgPathImage)
    return imagem.to_string(encoding="unicode")


def chave_para_digitar(device):
    """Segredo em base32, em grupos de 4, para quem não consegue ler o QR."""
    from base64 import b32encode

    chave = b32encode(device.bin_key).decode()
    return " ".join(chave[i : i + 4] for i in range(0, len(chave), 4))


def confirmar(device, token):
    """Confirma o app com o primeiro código. Devolve os códigos de recuperação, ou None."""
    if not device.verify_token(token):
        return None
    device.confirmed = True
    device.save()
    TOTPDevice.objects.filter(user=device.user, confirmed=False).delete()
    return gerar_codigos_de_recuperacao(device.user)


def gerar_codigos_de_recuperacao(user):
    StaticDevice.objects.filter(user=user).delete()
    estatico = StaticDevice.objects.create(user=user, name=NOME_RECUPERACAO, confirmed=True)
    codigos = [secrets.token_hex(4) for _ in range(QUANTIDADE_CODIGOS)]
    StaticToken.objects.bulk_create(StaticToken(device=estatico, token=c) for c in codigos)
    return codigos


def verificar(user, token):
    """Código do app ou de recuperação (este é gasto ao usar). Devolve o dispositivo ou None."""
    token = "".join(token.split()).lower()
    return match_token(user, token) if token else None
