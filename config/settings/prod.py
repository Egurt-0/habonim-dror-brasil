from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403
from .seguranca import TAMANHO_MINIMO_CHAVE, chave_secreta_fraca

DEBUG = False

if chave_secreta_fraca(SECRET_KEY):  # noqa: F405
    raise ImproperlyConfigured(
        f"DJANGO_SECRET_KEY é a de exemplo ou fraca. Gere uma com pelo menos "
        f"{TAMANHO_MINIMO_CHAVE} caracteres (ver .env.example)."
    )

# Em produção o endereço do admin tem que vir do ambiente; sem ele, o site não sobe.
ADMIN_URL = env("DJANGO_ADMIN_URL").strip("/") + "/"  # noqa: F405
if ADMIN_URL in ("admin/", "painel-dev/"):
    raise ImproperlyConfigured("DJANGO_ADMIN_URL precisa ser um endereço difícil de adivinhar.")

# WhiteNoise serve os arquivos estáticos em produção (logo depois do SecurityMiddleware).
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")  # noqa: F405

STORAGES["staticfiles"] = {  # noqa: F405
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
