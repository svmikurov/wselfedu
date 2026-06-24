"""Django site entrypoint DI container.

Defines which modules should be wired and provides the DI container
instance.
"""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from wse.site.handlers import ExerciseHandler


class DjangoSiteContainer(DeclarativeContainer):
    """Django site entrypoint DI container."""

    testing = Factory(
        ExerciseHandler,
    )
