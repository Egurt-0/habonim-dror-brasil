from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from . import services


class EntrarView(auth_views.LoginView):
    template_name = "contas/entrar.html"
    redirect_authenticated_user = True


class SairView(auth_views.LogoutView):
    pass


@require_POST
def seguir_sem_login(request):
    services.escolher_seguir_sem_login(request)
    destino = request.POST.get("next", "")
    if not url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}):
        destino = "core:home"
    return redirect(destino)
