from django.urls import path

from . import views

app_name = "movimento"

urlpatterns = [
    path("bases/", views.bases, name="bases"),
    path("shichavot-tzeirot/", views.shichavot_tzeirot, name="st"),
    path("shichavot-bogrot/", views.shichavot_bogrot, name="sb"),
    path("kehila-hd/", views.kehila_hd, name="kehila"),
]
