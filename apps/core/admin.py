from django.contrib import admin

from .models import BlocoTexto


@admin.register(BlocoTexto)
class BlocoTextoAdmin(admin.ModelAdmin):
    list_display = ["chave", "titulo", "updated_at"]
    search_fields = ["chave", "titulo", "texto"]
    readonly_fields = ["updated_at"]
