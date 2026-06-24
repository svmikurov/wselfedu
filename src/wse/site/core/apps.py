"""WSE application configuration."""

from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    """WSE application configuration."""

    name = 'wse.site.core'

    def ready(self) -> None:
        """Initialize the DI core container when Django starts."""
        from wse.di import django_site_container

        # Ensures that the container is created
        # only after Django is ready.
        if not settings.configured:
            return

        django_site_container.wire(modules=['.views'])
        print(f'{django_site_container.dependencies = }')
