from django.apps import AppConfig, apps
from django.db.models.signals import post_migrate


def _garantir_grupos(sender, **kwargs):
    # O post_migrate sai uma vez por app; só age no último, quando todas as permissões existem.
    com_models = [config for config in apps.get_app_configs() if config.models_module]
    if sender.label == com_models[-1].label:
        from .permissoes import garantir_grupos

        garantir_grupos()


class ContasConfig(AppConfig):
    name = "apps.contas"
    verbose_name = "Contas"

    def ready(self):
        post_migrate.connect(_garantir_grupos, dispatch_uid="contas.garantir_grupos")
