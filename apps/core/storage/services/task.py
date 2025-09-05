"""Defines clients for storing task."""

import logging
import uuid

from typing_extensions import override
from wse_exercises import TaskT

from ..clients.django_cache import DjangoCache
from .iabc import TaskStorageABC

logger = logging.getLogger(__name__)


class TaskStorage(TaskStorageABC[TaskT]):
    """Django cache storage task."""

    def __init__(
        self,
        storage: DjangoCache[TaskT],
    ) -> None:
        """Construct the storage."""
        self._storage = storage

    @override
    def save_task(self, obj: TaskT, ttl: int | None = None) -> uuid.UUID:
        """Save task to cache."""
        if ttl is None:
            ttl = 3600
        uid = self._storage.set(obj, ttl)
        return uid

    @override
    def retrieve_task(self, uid: uuid.UUID) -> TaskT:
        """Retrieve task."""
        try:
            task = self._storage.pop(uid)
            return task
        except Exception:
            logger.exception('Retrieve task error')
            raise
