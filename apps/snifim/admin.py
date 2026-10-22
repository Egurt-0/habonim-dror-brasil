from django.contrib import admin

from .models import Kehila, Snif


@admin.register(Snif)
class SnifAdmin(admin.ModelAdmin):
    list_display = ["nome", "estado", "ano_fundacao", "instagram", "tem_cchd", "ativo"]
    list_filter = ["ativo", "tem_cchd", "estado"]
    list_editable = ["instagram"]
    search_fields = ["nome", "cidade"]
    prepopulated_fields = {"slug": ["nome"]}


@admin.register(Kehila)
class KehilaAdmin(admin.ModelAdmin):
    list_display = ["nome", "cidade", "site"]
    search_fields = ["nome", "cidade"]
