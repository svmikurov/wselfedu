"""Defines clients for storing task."""

import hashlib
import logging
from typing import Hashable, TypeVar, override

from apps.core.exceptions.storage import (
    CacheMissError,
    StorageProgrammingError,
)

from ..clients.django_cache import DjangoKeyCache
from .iabc import AbstractUserStorage

T = TypeVar('T', bound=Hashable)

logger = logging.getLogger(__name__)

DEFAULT_TTL = 3600
HASH_SYMBOL_COUNT = 8


def generate_cache_key(prefix: str, user_id: int, **kwargs: object) -> str:
    """Generate a secure key with parameter hashing."""
    sorted_items = sorted(kwargs.items())
    param_string = ':'.join([f'{k}:{v}' for k, v in sorted_items])
    param_hash = hashlib.md5(param_string.encode()).hexdigest()[
        :HASH_SYMBOL_COUNT
    ]
    return f'{prefix}:{user_id}:{param_hash}'


class UserDataStorage(AbstractUserStorage[T]):
    """User's data storage."""

    def __init__(
        self,
        storage: DjangoKeyCache[T],
        ttl: int | None = None,
    ) -> None:
        """Construct the storage."""
        self._storage = storage
        self.ttl = ttl or DEFAULT_TTL

    @override
    def save(
        self,
        obj: T,
        user_pk: int,
        prefix: str,
        ttl: int | None = None,
        **kwargs: object,
    ) -> None:
        """Save user's data."""
        cache_key = generate_cache_key(prefix, user_pk, **kwargs)
        if ttl is None:
            ttl = self.ttl
        self._storage.set(obj, cache_key, ttl)

    @override
    def retrieve(self, user_pk: int, prefix: str, **kwargs: object) -> T:
        """Retrieve user's data."""
        cache_key = generate_cache_key(prefix, user_pk, **kwargs)

        try:
            return self._storage.pop(cache_key)

        except KeyError:
            logger.debug('Cache miss for key: %s', cache_key)
            raise CacheMissError(
                f'No data found for key: {cache_key}'
            ) from None

        except Exception as exc:
            logger.exception('Cache technical error for key: %s', cache_key)
            raise StorageProgrammingError(
                'Failed to retrieve from cache'
            ) from exc
