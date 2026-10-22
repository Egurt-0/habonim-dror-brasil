from django.contrib import admin

from .models import Termo


@admin.register(Termo)
class TermoAdmin(admin.ModelAdmin):
    list_display = ["termo", "definicao", "variantes"]
    search_fields = ["termo", "definicao", "variantes"]
    prepopulated_fields = {"slug": ["termo"]}
