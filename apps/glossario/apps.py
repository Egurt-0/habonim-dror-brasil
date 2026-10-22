from django.apps import AppConfig


class GlossarioConfig(AppConfig):
    name = "apps.glossario"
    verbose_name = "Glossário"

    def ready(self):
        from . import signals  # noqa: F401
