"""Defines main app config."""

from django.apps import AppConfig
from django.conf import settings


class MainConfig(AppConfig):
    """Main app config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.main'

    verbose_name = 'Основное приложение'

    def ready(self) -> None:
        """Initialize the DI core container when Django starts."""
        from di import WIRED_MODULES, container

        # Ensures that the container is created
        # only after Django is ready.
        if not settings.configured:
            return

        container.wire(modules=WIRED_MODULES)
