"""Contains storage services."""

__all__ = [
    # Abstract / Protocol
    'StorageClient',
    'TaskStorageABC',
    # Real
    'DjangoCache',
    'TaskStorage',
]

from ports.contract.infra.storage.task import TaskStorage

from .clients import DjangoCache
from .clients.iabc import StorageClient
from .services.iabc import TaskStorageABC
