"""Core application dependency injection container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container, Factory

from ..storage.clients.django_cache import DjangoCache
from ..storage.services.task import TaskStorage
from .configuration import ConfigurationContainer
from .domain import DomainContainer


class CoreContainer(DeclarativeContainer):
    """Core application dependency injection container."""

    configuration = Container(
        ConfigurationContainer,
    )

    domains = Container(
        DomainContainer,
        exercise_config=configuration.exercise,
    )

    django_cache = Factory(  # type: ignore[var-annotated]
        DjangoCache,
    )

    # TODO: Rename to `django_cache`?
    task_storage = Factory(
        TaskStorage,
        storage=django_cache,
    )
