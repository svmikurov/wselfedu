"""Defines Core app config."""

from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    """Core app config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'

    verbose_name = 'Базовое приложение'

    def ready(self) -> None:
        """Initialize the DI core container when Django starts."""
        from di import WIRED_MODULES, container

        # Ensures that the container is created
        # only after Django is ready.
        if not settings.configured:
            return

        container.wire(modules=WIRED_MODULES)
