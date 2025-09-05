"""Defines Core app DI container."""

from typing import Any

from dependency_injector import containers, providers
from dependency_injector.providers import Factory

from .storage.clients.django_cache import DjangoCache
from .storage.services.task import TaskStorage


class CoreContainer(containers.DeclarativeContainer):
    """DI container for Core app dependencies."""

    cache_task_storage: Factory[DjangoCache[Any]] = providers.Factory(
        DjangoCache,
    )

    task_storage = providers.Factory(
        TaskStorage,
        storage=cache_task_storage,
    )
