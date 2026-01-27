"""DI container for Storage."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory

from apps.core import storage

if TYPE_CHECKING:
    type StorageClientFactory = Factory[storage.StorageClient[Any]]
    type CaseStorageFactory = Factory[storage.TaskStorageABC[Any]]


class StorageContainer(DeclarativeContainer):
    """DI container for Storage."""

    config = Configuration()
    """Exercise case storage configuration.
    """

    # HACK: Reorganize exercise case storage settings definition
    config.from_dict(
        {
            'case_storage_ttl': 600,
        }
    )

    cache_client: StorageClientFactory = Factory(storage.DjangoCache)

    exercise_case_storage: CaseStorageFactory = Factory(
        storage.TaskStorage,
        storage=cache_client,
        ttl=config.case_storage_ttl,
    )
