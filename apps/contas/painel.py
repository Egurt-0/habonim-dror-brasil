"""Painel (admin) que exige verificação em duas etapas (2FA) de toda conta da equipe.

A senha sozinha não abre o painel: depois do login, a pessoa digita o código do aplicativo
autenticador (ou um código de recuperação). Quem ainda não tem 2FA é levado a configurar.
Ligado em INSTALLED_APPS via PainelAdminConfig (substitui "django.contrib.admin").
"""

from urllib.parse import urlencode

from django.contrib import admin
from django.contrib.admin.apps import AdminConfig
from django.shortcuts import redirect
from django.urls import reverse


class PainelAdminSite(admin.AdminSite):
    site_header = "Habonim Dror Brasil"
    site_title = "Painel HDBR"
    index_title = "Conteúdo do site"

    def has_permission(self, request):
        return super().has_permission(request) and request.user.is_verified()

    def login(self, request, extra_context=None):
        user = request.user
        if user.is_authenticated and user.is_active and user.is_staff and not user.is_verified():
            destino = request.GET.get("next") or reverse("admin:index", current_app=self.name)
            return redirect(f"{reverse('contas:verificar_2fa')}?{urlencode({'next': destino})}")
        return super().login(request, extra_context)


class PainelAdminConfig(AdminConfig):
    default_site = "apps.contas.painel.PainelAdminSite"
