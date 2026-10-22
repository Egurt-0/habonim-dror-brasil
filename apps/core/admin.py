from django.contrib import admin

from .models import BlocoTexto, Topico


@admin.register(BlocoTexto)
class BlocoTextoAdmin(admin.ModelAdmin):
    list_display = ["chave", "titulo", "updated_at"]
    search_fields = ["chave", "titulo", "texto"]
    readonly_fields = ["updated_at"]


@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ["titulo", "link", "ordem", "ativo"]
    list_editable = ["ordem", "ativo"]
    prepopulated_fields = {"slug": ["titulo"]}
