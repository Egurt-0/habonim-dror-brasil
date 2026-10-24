from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from . import services
from .forms import CadastroForm, EsqueciSenhaForm


class EntrarView(auth_views.LoginView):
    template_name = "contas/entrar.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        return super().get_context_data(cadastro_aberto=settings.CADASTRO_ABERTO, **kwargs)


class SairView(auth_views.LogoutView):
    def post(self, request, *args, **kwargs):
        resposta = super().post(request, *args, **kwargs)
        # O logout apaga a sessão; quem saiu já escolheu como entrar, não perguntar de novo.
        services.escolher_seguir_sem_login(request)
        return resposta


def _destino_seguro(request, destino):
    """Só aceita caminhos internos (começando com '/'); qualquer outra coisa vai para a home."""
    if destino.startswith("/") and url_has_allowed_host_and_scheme(
        destino, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return destino
    return reverse("core:home")


@require_POST
def seguir_sem_login(request):
    services.escolher_seguir_sem_login(request)
    return redirect(_destino_seguro(request, request.POST.get("next", "")))


def cadastro(request):
    if request.user.is_authenticated:
        return redirect("core:home")
    if not settings.CADASTRO_ABERTO:
        return render(request, "contas/cadastro.html", {"fechado": True})
    form = CadastroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        services.cadastrar(form.cleaned_data["first_name"], form.cleaned_data["email"])
        return redirect("contas:cadastro_enviado")
    return render(request, "contas/cadastro.html", {"form": form})


class AtivarContaView(auth_views.PasswordResetConfirmView):
    """Link do e-mail de cadastro: a pessoa cria a senha e a conta é ativada."""

    token_generator = services.gerador_de_ativacao
    form_class = SetPasswordForm
    template_name = "contas/ativar.html"
    success_url = reverse_lazy("contas:entrar")
    reset_url_token = "criar-senha"

    def form_valid(self, form):
        form.user.is_active = True  # salvo junto com a senha por form.save()
        resposta = super().form_valid(form)
        messages.success(self.request, "Conta ativada. Agora é só entrar com seu e-mail e senha.")
        return resposta


class EsqueciSenhaView(auth_views.PasswordResetView):
    form_class = EsqueciSenhaForm
    template_name = "contas/esqueci_senha.html"
    success_url = reverse_lazy("contas:esqueci_senha_enviado")


class RedefinirSenhaView(auth_views.PasswordResetConfirmView):
    template_name = "contas/redefinir_senha.html"
    success_url = reverse_lazy("contas:entrar")

    def form_valid(self, form):
        resposta = super().form_valid(form)
        messages.success(self.request, "Senha alterada. Entre com a nova senha.")
        return resposta
