"""DI container for Core app."""

from typing import Any

from dependency_injector import containers, providers
from dependency_injector.providers import Factory

from apps.core.storage.task import DjangoCache, TaskStorage


class CoreContainer(containers.DeclarativeContainer):
    """DI container for Core app."""

    cache_task_storage: Factory[DjangoCache[Any]] = providers.Factory(
        DjangoCache,
    )

    task_storage = providers.Factory(
        TaskStorage,
        storage=cache_task_storage,
    )
