"""Defines Core application config."""

from django.apps import AppConfig
from django.conf import settings

MODULES_TO_WIRE = [
    'apps.mathem.api.v1.views',
]


class CoreConfig(AppConfig):
    """Core application config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.main'

    def ready(self) -> None:
        """Initialize the DI main container when Django starts."""
        # Ensures that the container is created
        # only after Django is ready.
        if not settings.configured:
            return

        from di.di_initialization import init_container

        init_container(MODULES_TO_WIRE)
