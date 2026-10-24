from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    list_display = ["email", "first_name", "last_name", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_superuser", "is_active", "groups"]
    search_fields = ["email", "first_name", "last_name"]
    filter_horizontal = ["groups", "user_permissions", "snifim"]
    readonly_fields = [
        "last_login",
        "date_joined",
        "aceitou_privacidade_em",
        "declarou_maioridade_em",
    ]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Dados pessoais", {"fields": ["first_name", "last_name"]}),
        (
            "Permissões",
            {
                "fields": ["is_active", "is_staff", "is_superuser", "groups", "snifim"],
                "description": (
                    "Para editar o painel: marque “membro da equipe” e escolha um grupo. "
                    "editor_nacional edita todo o conteúdo; editor_snif edita só os snifim "
                    "marcados abaixo. Superusuário: só para 1 ou 2 pessoas."
                ),
            },
        ),
        (
            "Permissões avulsas (evite: prefira os grupos)",
            {"classes": ["collapse"], "fields": ["user_permissions"]},
        ),
        (
            "Datas e aceites (LGPD)",
            {
                "fields": [
                    "last_login",
                    "date_joined",
                    "aceitou_privacidade_em",
                    "declarou_maioridade_em",
                ]
            },
        ),
    ]
    add_fieldsets = [
        (None, {"classes": ["wide"], "fields": ["email", "password1", "password2"]}),
    ]
