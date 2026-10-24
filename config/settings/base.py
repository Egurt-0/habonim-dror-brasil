"""Configurações comuns a todos os ambientes. Valores sensíveis vêm do .env."""

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_ALLOWED_HOSTS=(list, []),
    DJANGO_CSRF_TRUSTED_ORIGINS=(list, []),
    DJANGO_ATRAS_DE_PROXY=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env("DJANGO_CSRF_TRUSTED_ORIGINS")

# Endereço do painel admin. Nunca "admin/": vem do .env para não ficar no código público.
# Em produção é obrigatório (prod.py não tem valor padrão).
ADMIN_URL = env("DJANGO_ADMIN_URL", default="painel-dev/").strip("/") + "/"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "axes",
    # apps do projeto
    "apps.contas",
    "apps.core",
    "apps.glossario",
    "apps.movimento",
    "apps.snifim",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",  # tem que ser o último
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["CONN_MAX_AGE"] = 60

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Contas
AUTH_USER_MODEL = "contas.User"
LOGIN_URL = "contas:entrar"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",  # recusa login de quem está bloqueado
    "django.contrib.auth.backends.ModelBackend",
]

# Bloqueio após senhas erradas (django-axes), no login do site e no do admin.
# Conta por e-mail + IP: errar a senha de alguém não bloqueia essa pessoa em outro lugar.
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # horas (o texto de contas/bloqueado.html fala em 1 hora)
AXES_LOCKOUT_PARAMETERS = [["username", "ip_address"]]
# O formulário de login do Django manda o e-mail no campo "username" (o padrão do axes seria
# "email", o USERNAME_FIELD). Sem isto o e-mail não é registrado e a senha certa passaria.
AXES_USERNAME_FORM_FIELD = "username"
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_TEMPLATE = "contas/bloqueado.html"
AXES_CLIENT_IP_CALLABLE = "apps.contas.services.ip_do_cliente"
# True só quando o site roda atrás de um proxy (nginx etc.) que preenche X-Forwarded-For.
ATRAS_DE_PROXY = env("DJANGO_ATRAS_DE_PROXY")

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Idioma e fuso
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Arquivos estáticos e mídia
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
