"""Core generic repositories."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypedDict, TypeVar, override

from apps.core.assemblers.protocol import UserDetailCommandProtocol
from apps.core.exceptions.storage import CacheMissError
from apps.core.repositories.abstract import AbstractRepository

if TYPE_CHECKING:
    from apps.core.storages.services.iabc import AbstractUserStorage

__all__ = ('UserResourceRepository',)

FilterData = TypeVar('FilterData', bound=UserDetailCommandProtocol)
QueryResult = TypeVar('QueryResult')


class CacheKeyDict(TypedDict):
    """Typed dict for cache key."""

    user_pk: int
    prefix: str
    resource_pk: int


class UserResourceRepository(
    AbstractRepository[FilterData, QueryResult],
    Generic[FilterData, QueryResult],
):
    """Base user's resource repository."""

    def __init__(
        self,
        store_prefix: str,
        storage: AbstractUserStorage[QueryResult],
    ) -> None:
        """Construct the repository."""
        self._store_prefix = store_prefix
        self._storage = storage

    @override
    def fetch(self, filter: FilterData) -> QueryResult:
        """Fetch resource."""
        key_kwargs = self._get_key(filter.user.pk, filter.pk)

        try:
            return self._storage.retrieve(**key_kwargs)
        except CacheMissError:
            obj = self._get_object(filter)
            self._storage.save(obj, **key_kwargs)
            return obj

    def _get_key(self, user_pk: int, resource_pk: int) -> CacheKeyDict:
        return {
            'user_pk': user_pk,
            'prefix': self._store_prefix,
            'resource_pk': resource_pk,
        }

    def _get_object(self, command: FilterData) -> QueryResult:
        raise NotImplementedError('Subclass must implement _get_object()')
