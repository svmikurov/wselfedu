"""Contains storage services."""

__all__ = [
    # Abstract / Protocol
    'StorageClient',
    'TaskStorageABC',
    # Real
    'DjangoCache',
    'TaskStorage',
]

from .clients import DjangoCache
from .clients.iabc import StorageClient
from .services.iabc import TaskStorageABC
from .services.task import TaskStorage
