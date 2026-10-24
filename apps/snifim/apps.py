from django.apps import AppConfig


class SnifimConfig(AppConfig):
    name = "apps.snifim"
    verbose_name = "Snifim"

    def ready(self):
        from . import signals  # noqa: F401
