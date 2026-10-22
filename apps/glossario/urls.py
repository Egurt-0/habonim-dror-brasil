from django.urls import path

from . import views

app_name = "glossario"

urlpatterns = [
    path("", views.lista, name="lista"),
]
