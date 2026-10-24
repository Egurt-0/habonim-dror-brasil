import json
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django_otp import login as otp_login

from . import dois_fatores, services
from .forms import CadastroForm, CodigoForm, EsqueciSenhaForm, ExcluirContaForm, MeusDadosForm


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


@login_required
def meus_dados(request):
    user = request.user
    form = MeusDadosForm(
        request.POST or None, initial={"first_name": user.first_name, "last_name": user.last_name}
    )
    if request.method == "POST" and form.is_valid():
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.save(update_fields=["first_name", "last_name"])
        messages.success(request, "Dados atualizados.")
        return redirect("contas:meus_dados")
    contexto = {"form": form, "pode_excluir": services.pode_excluir_pelo_site(user)}
    return render(request, "contas/meus_dados.html", contexto)


@login_required
def baixar_dados(request):
    conteudo = json.dumps(services.dados_do_usuario(request.user), ensure_ascii=False, indent=2)
    resposta = HttpResponse(conteudo, content_type="application/json; charset=utf-8")
    resposta["Content-Disposition"] = 'attachment; filename="meus-dados-habonim-dror.json"'
    return resposta


@login_required
def excluir_conta(request):
    user = request.user
    if not services.pode_excluir_pelo_site(user):
        messages.error(request, "Contas do painel são excluídas por um administrador.")
        return redirect("contas:meus_dados")
    form = ExcluirContaForm(user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        logout(request)
        services.excluir_conta(user)
        messages.success(request, "Sua conta e seus dados foram excluídos.")
        return redirect("core:home")
    return render(request, "contas/excluir_conta.html", {"form": form})


class TrocarSenhaView(auth_views.PasswordChangeView):
    template_name = "contas/trocar_senha.html"
    success_url = reverse_lazy("contas:meus_dados")

    def form_valid(self, form):
        resposta = super().form_valid(form)  # mantém a pessoa logada com a senha nova
        messages.success(self.request, "Senha alterada.")
        return resposta


class RedefinirSenhaView(auth_views.PasswordResetConfirmView):
    template_name = "contas/redefinir_senha.html"
    success_url = reverse_lazy("contas:entrar")

    def form_valid(self, form):
        resposta = super().form_valid(form)
        messages.success(self.request, "Senha alterada. Entre com a nova senha.")
        return resposta


# Verificação em duas etapas (equipe do painel) ---------------------------------------------

MENSAGEM_CODIGO_ERRADO = (
    "Código inválido ou expirado. Depois de vários erros é preciso esperar um pouco para tentar "
    "de novo."
)


def _equipe(request):
    if not request.user.is_staff:
        raise PermissionDenied


def _destino_do_painel(request):
    destino = request.POST.get("next") or request.GET.get("next") or reverse("admin:index")
    return _destino_seguro(request, destino)


@never_cache
@login_required
def verificar_2fa(request):
    _equipe(request)
    destino = _destino_do_painel(request)
    if request.user.is_verified():
        return redirect(destino)
    if not dois_fatores.tem_2fa(request.user):
        return redirect(f"{reverse('contas:configurar_2fa')}?{urlencode({'next': destino})}")
    form = CodigoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        device = dois_fatores.verificar(request.user, form.cleaned_data["codigo"])
        if device:
            otp_login(request, device)
            return redirect(destino)
        form.add_error("codigo", MENSAGEM_CODIGO_ERRADO)
    return render(request, "contas/2fa_verificar.html", {"form": form, "next": destino})


@never_cache
@login_required
def configurar_2fa(request):
    _equipe(request)
    user = request.user
    destino = _destino_do_painel(request)
    if dois_fatores.tem_2fa(user) and not user.is_verified():
        # Quem já tem 2FA prova que tem o celular antes de trocar (senha roubada não basta).
        return redirect(f"{reverse('contas:verificar_2fa')}?{urlencode({'next': destino})}")
    device = dois_fatores.dispositivo_em_configuracao(user)
    form = CodigoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        codigos = dois_fatores.confirmar(device, form.cleaned_data["codigo"])
        if codigos:
            otp_login(request, device)
            contexto = {"codigos": codigos, "next": destino}
            return render(request, "contas/2fa_codigos.html", contexto)
        form.add_error("codigo", MENSAGEM_CODIGO_ERRADO)
    contexto = {
        "form": form,
        "next": destino,
        "qr": dois_fatores.qr_svg(device),
        "chave": dois_fatores.chave_para_digitar(device),
    }
    return render(request, "contas/2fa_configurar.html", contexto)
