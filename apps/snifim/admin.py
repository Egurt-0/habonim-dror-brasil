from django.contrib import admin
from django.utils.html import format_html

from .models import Bagrut, FotoSnif, Kehila, Snif


def _previa(campo, altura=80):
    if not campo:
        return "—"
    return format_html('<img src="{}" alt="" style="height:{}px">', campo.url, altura)


class FotoSnifInline(admin.TabularInline):
    model = FotoSnif
    extra = 1
    fields = ["previa", "imagem", "alt", "legenda", "data", "ordem", "autorizada"]
    readonly_fields = ["previa"]

    @admin.display(description="prévia")
    def previa(self, obj):
        return _previa(obj.miniatura or obj.imagem)


class BagrutInline(admin.StackedInline):
    model = Bagrut
    extra = 0
    fields = ["gestao", "atual", "descricao", "previa", "foto", "foto_alt", "autorizada"]
    readonly_fields = ["previa"]

    @admin.display(description="prévia")
    def previa(self, obj):
        return _previa(obj.foto, 120)


@admin.register(Snif)
class SnifAdmin(admin.ModelAdmin):
    list_display = ["nome", "estado", "ano_fundacao", "instagram", "tem_cchd", "ativo"]
    list_filter = ["ativo", "tem_cchd", "estado"]
    list_editable = ["instagram"]
    search_fields = ["nome", "cidade"]
    prepopulated_fields = {"slug": ["nome"]}
    inlines = [BagrutInline, FotoSnifInline]
    readonly_fields = ["previa_capa"]
    fieldsets = [
        (None, {"fields": ["nome", "slug", "cidade", "estado", "ano_fundacao", "ativo"]}),
        ("Texto da página", {"fields": ["resumo", "historia"]}),
        ("Foto de capa", {"fields": ["previa_capa", "foto_capa", "foto_capa_alt"]}),
        ("Contato", {"fields": ["instagram", "contato", "endereco"]}),
        ("Parceiros", {"fields": ["kehila", "tem_cchd", "cchd_descricao"]}),
    ]

    @admin.display(description="prévia")
    def previa_capa(self, obj):
        return _previa(obj.foto_capa, 120)


@admin.register(Kehila)
class KehilaAdmin(admin.ModelAdmin):
    list_display = ["nome", "cidade", "site"]
    search_fields = ["nome", "cidade"]
