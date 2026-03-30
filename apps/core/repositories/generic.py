"""Core generic repositories."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypedDict, TypeVar, override

from apps.core.assemblers.protocol import (
    UserCommandProtocol,
    UserDetailCommandProtocol,
)
from apps.core.exceptions.storage import CacheMissError
from apps.core.repositories.abstract import AbstractRepository

if TYPE_CHECKING:
    from apps.core.storages.services.iabc import AbstractUserStorage

__all__ = ('UserResourceCachedRepository',)

FilterUser = TypeVar('FilterUser', bound=UserCommandProtocol)
FilterUserData = TypeVar('FilterUserData', bound=UserDetailCommandProtocol)
QueryResult = TypeVar('QueryResult')


class _CacheKey(TypedDict):
    """Typed dict for cache key."""

    user_pk: int
    prefix: str


class _ResourceCacheKey(_CacheKey):
    """Typed dict for resource cache key."""

    resource_pk: int


class _Repository(
    AbstractRepository[FilterUser, QueryResult],
    Generic[FilterUser, QueryResult],
):
    """Base repository."""

    def __init__(
        self,
        store_prefix: str,
        storage: AbstractUserStorage[QueryResult],
    ) -> None:
        """Construct the repository."""
        self._store_prefix = store_prefix
        self._storage = storage

    def _get_object(self, command: FilterUser) -> QueryResult:
        raise NotImplementedError('Subclass must implement _get_object()')


class UserCachedRepository(
    _Repository[FilterUser, QueryResult],
    Generic[FilterUser, QueryResult],
):
    """Base user's resource repository."""

    @override
    def fetch(self, filter: FilterUser) -> QueryResult:  # type: ignore
        """Fetch resource."""
        key_kwargs = self._get_key(filter.user.pk)

        try:
            return self._storage.retrieve(**key_kwargs)
        except CacheMissError:
            obj = self._get_object(filter)
            self._storage.save(obj, **key_kwargs)
            return obj

    def _get_key(self, user_pk: int) -> _CacheKey:
        return {
            'user_pk': user_pk,
            'prefix': self._store_prefix,
        }


class UserResourceCachedRepository(
    _Repository[FilterUserData, QueryResult],
    Generic[FilterUserData, QueryResult],
):
    """Base user's resource repository."""

    @override
    def fetch(self, filter: FilterUserData) -> QueryResult:  # type: ignore
        """Fetch resource."""
        key_kwargs = self._get_key(filter.user.pk, filter.pk)

        try:
            return self._storage.retrieve(**key_kwargs)
        except CacheMissError:
            obj = self._get_object(filter)
            self._storage.save(obj, **key_kwargs)
            return obj

    def _get_key(self, user_pk: int, resource_pk: int) -> _ResourceCacheKey:
        return {
            'user_pk': user_pk,
            'prefix': self._store_prefix,
            'resource_pk': resource_pk,
        }
