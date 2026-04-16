"""Defines clients for storing task."""

import logging
from typing import Hashable, TypeVar, override

from apps.core.assemblers.command import UserCommand
from apps.core.exceptions.storage import (
    CacheMissError,
    StorageProgrammingError,
)
from apps.core.storages.abstract import AbstractStoreKeyResolver
from apps.core.storages.services.iabc import AbstractCommandStorage

from ..clients.django_cache import DjangoKeyCache
from ..resolver import generate_cache_key
from .iabc import AbstractUserStorage

T = TypeVar('T', bound=Hashable)
StoredObject = TypeVar('StoredObject')
Command = TypeVar('Command')

logger = logging.getLogger(__name__)

DEFAULT_TTL = 3600


class UserCommandStorage(
    AbstractCommandStorage[
        StoredObject,
        UserCommand,
    ],
):
    """User's command related data storage."""

    def __init__(
        self,
        storage: DjangoKeyCache[StoredObject],
        key_resolver: AbstractStoreKeyResolver[UserCommand, str],
        ttl: int | None = None,
    ) -> None:
        """Construct the storage."""
        self._storage = storage
        self._key_resolver = key_resolver
        self.ttl = ttl or DEFAULT_TTL

    @override
    def save(  # type: ignore
        self,
        command: UserCommand,
        obj: StoredObject,
        prefix: str,
        ttl: int | None = None,
        **kwargs: object,
    ) -> None:
        """Save user's data."""
        cache_key = self._key_resolver.resolve(command, prefix, **kwargs)

        if ttl is None:
            ttl = self.ttl
        self._storage.set(obj, cache_key, ttl)

    @override
    def retrieve(  # type: ignore
        self,
        command: UserCommand,  # type: ignore
        prefix: str,
        **kwargs: object,
    ) -> StoredObject:
        """Retrieve user's data."""
        cache_key = self._key_resolver.resolve(command, prefix, **kwargs)

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
