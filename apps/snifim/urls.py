from django.urls import path

from . import views

app_name = "snifim"

urlpatterns = [
    path("snifim/", views.lista, name="lista"),
    path("snifim/<slug:slug>/", views.detalhe, name="detalhe"),
    path("quero-saber-mais/", views.quero_saber_mais, name="saber_mais"),
]
