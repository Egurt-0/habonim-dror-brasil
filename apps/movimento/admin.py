from django.contrib import admin

from .models import Numero, Pilar, ReferenciaPedagogica, Tochnit


@admin.register(Pilar)
class PilarAdmin(admin.ModelAdmin):
    list_display = ["nome", "subtitulo", "ordem"]
    list_editable = ["ordem"]
    prepopulated_fields = {"slug": ["nome"]}


@admin.register(ReferenciaPedagogica)
class ReferenciaPedagogicaAdmin(admin.ModelAdmin):
    list_display = ["nome", "ordem"]
    list_editable = ["ordem"]


@admin.register(Tochnit)
class TochnitAdmin(admin.ModelAdmin):
    list_display = ["nome", "temas", "ordem"]
    list_editable = ["ordem"]


@admin.register(Numero)
class NumeroAdmin(admin.ModelAdmin):
    list_display = ["valor", "prefixo", "rotulo", "destaque", "ordem"]
    list_editable = ["destaque", "ordem"]
