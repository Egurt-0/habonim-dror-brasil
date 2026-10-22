from django.urls import path

from . import views

app_name = "contas"

urlpatterns = [
    path("entrar/", views.EntrarView.as_view(), name="entrar"),
    path("sair/", views.SairView.as_view(), name="sair"),
    path("sem-login/", views.seguir_sem_login, name="sem_login"),
]
