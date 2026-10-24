from django.contrib import admin

from .models import BlocoTexto, Topico

AJUDA_ANOS = (
    "Escreva {anos} onde deve aparecer a idade do movimento: o site calcula sozinho a partir "
    "de 1945 (ex.: “{anos} anos de história”)."
)


@admin.register(BlocoTexto)
class BlocoTextoAdmin(admin.ModelAdmin):
    list_display = ["chave", "titulo", "updated_at"]
    search_fields = ["chave", "titulo", "texto"]
    readonly_fields = ["updated_at"]
    fieldsets = [
        (None, {"fields": ["chave", "titulo", "texto", "updated_at"], "description": AJUDA_ANOS})
    ]


@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ["titulo", "link", "ordem", "ativo"]
    list_editable = ["ordem", "ativo"]
    prepopulated_fields = {"slug": ["titulo"]}
    fieldsets = [
        (
            None,
            {
                "fields": ["titulo", "slug", "resumo", "link", "ordem", "ativo"],
                "description": AJUDA_ANOS,
            },
        )
    ]
