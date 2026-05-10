"""Storage DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory

from apps.core import storages


class StorageContainer(DeclarativeContainer):
    """Storage DI container."""

    # External dependencies
    # ---------------------

    config = Configuration()

    # Dependency factory
    # ------------------

    cache_client = Factory(  # type: ignore[var-annotated]
        storages.DjangoCache,
    )

    exercise_case_storage = Factory(
        storages.TaskStorage,
        storage=cache_client,
        ttl=config.case_storage_ttl,
    )
