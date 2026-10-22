from django.urls import path

from . import views

app_name = "snifim"

urlpatterns = [
    path("quero-saber-mais/", views.quero_saber_mais, name="saber_mais"),
]
