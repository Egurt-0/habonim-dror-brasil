"""Liga a limpeza de arquivos (services.py) ao save/delete dos models com foto."""

from django.db.models.signals import post_delete, post_save, pre_save

from . import services
from .models import Bagrut, FotoSnif, Snif


def _antes_de_salvar(sender, instance, raw=False, **kwargs):
    if not raw:
        services.lembrar_arquivos_atuais(instance)


def _depois_de_salvar(sender, instance, raw=False, **kwargs):
    if not raw:
        services.apagar_arquivos_substituidos(instance)


def _depois_de_excluir(sender, instance, **kwargs):
    services.apagar_arquivos(instance)


for model in (Snif, FotoSnif, Bagrut):
    pre_save.connect(_antes_de_salvar, sender=model)
    post_save.connect(_depois_de_salvar, sender=model)
    post_delete.connect(_depois_de_excluir, sender=model)
