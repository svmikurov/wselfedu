"""Defines clients for storing task."""

import logging
import uuid
from typing import Generic, TypeVar, override

from ..clients.django_cache import DjangoCache
from .iabc import TaskStorageABC

logger = logging.getLogger(__name__)

T = TypeVar('T')


class TaskStorage(Generic[T], TaskStorageABC[T]):
    """Django cache storage task."""

    DEFAULT_TTL = 3600

    def __init__(
        self,
        storage: DjangoCache[T],
        ttl: int | None = None,
    ) -> None:
        """Construct the storage."""
        self._storage = storage
        self.ttl = ttl or self.DEFAULT_TTL

    @override
    def save_task(self, obj: T, ttl: int | None = None) -> uuid.UUID:
        """Save task to cache."""
        if ttl is None:
            ttl = self.ttl
        uid = self._storage.set(obj, ttl)
        return uid

    @override
    def retrieve_task(self, uid: uuid.UUID) -> T:
        """Retrieve task."""
        try:
            task = self._storage.pop(uid)
            return task
        except Exception:
            logger.exception('Retrieve task error')
            raise
