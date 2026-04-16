"""Abstract base class for repository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar, override

from .protocol import UserRepositoryProtocol

if TYPE_CHECKING:
    from apps.users.models import Person

FilterT = TypeVar('FilterT')
ResultT = TypeVar('ResultT')


class AbstractUserFetchRepository(
    ABC,
    UserRepositoryProtocol[FilterT, ResultT],
):
    """ABC for fetch repository via user filter."""

    @override
    @abstractmethod
    def fetch(self, user: Person, filter: FilterT) -> ResultT:
        """Fetch."""
