from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from . import services


class EntrarView(auth_views.LoginView):
    template_name = "contas/entrar.html"
    redirect_authenticated_user = True


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
