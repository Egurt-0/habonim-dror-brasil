from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "contas"

urlpatterns = [
    path("entrar/", views.EntrarView.as_view(), name="entrar"),
    path("sair/", views.SairView.as_view(), name="sair"),
    path("sem-login/", views.seguir_sem_login, name="sem_login"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path(
        "cadastro/enviado/",
        TemplateView.as_view(template_name="contas/cadastro_enviado.html"),
        name="cadastro_enviado",
    ),
    path("ativar/<uidb64>/<token>/", views.AtivarContaView.as_view(), name="ativar"),
    path("senha/esqueci/", views.EsqueciSenhaView.as_view(), name="esqueci_senha"),
    path(
        "senha/esqueci/enviado/",
        TemplateView.as_view(template_name="contas/esqueci_senha_enviado.html"),
        name="esqueci_senha_enviado",
    ),
    path(
        "senha/redefinir/<uidb64>/<token>/",
        views.RedefinirSenhaView.as_view(),
        name="redefinir_senha",
    ),
]
