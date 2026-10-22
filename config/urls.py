from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Habonim Dror Brasil"
admin.site.site_title = "Painel HDBR"
admin.site.index_title = "Conteúdo do site"

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("contas/", include("apps.contas.urls")),
    path("glossario/", include("apps.glossario.urls")),
    path("", include("apps.movimento.urls")),
    path("", include("apps.snifim.urls")),
    path("", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
