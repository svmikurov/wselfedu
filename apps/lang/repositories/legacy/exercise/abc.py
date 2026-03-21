"""Abstract base classes for translation exercise repository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from apps.lang.schemas import ParametersSchema
    from apps.users.models import Person

T = TypeVar('T')


class ByUserRepositoryABC(ABC, Generic[T]):
    """ABC repository to fetch items by user."""

    @abstractmethod
    def fetch(self, user: Person) -> T:
        """Get items by user."""


class CandidatesRepositoryABC(ABC, Generic[T]):
    """ABC repository to fetch candidates for exercise."""

    @abstractmethod
    def fetch(self, user: Person, conditions: ParametersSchema) -> T:
        """Fetch candidates for exercise by conditions."""
