"""Infrastructure DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from wse.infrastructure import repositories


class InfrastructureContainer(DeclarativeContainer):
    """Infrastructure DI container."""

    learnable = Factory(repositories.InMemoryLearnableRepository)
    task = Factory(repositories.InMemoryLearnableRepository)
