"""Abstract base classes fot core repository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from apps.core.domains.exercise.types import Candidates, Parameters
    from apps.users.models import Person

__all__ = [
    'AbstractByUserQueryRepository',
    'AbstractUserConditionsRepository',
    'AbstractDetailExerciseRepository',
]

LookupConditions = TypeVar('LookupConditions')
QueryResult = TypeVar('QueryResult')


class AbstractByUserQueryRepository(ABC):
    """ABC for repository to query by user."""

    @abstractmethod
    def fetch(self, user: Person) -> Parameters:
        """Fetch user's data."""


class AbstractUserConditionsRepository(
    ABC, Generic[LookupConditions, QueryResult]
):
    """ABC for repository to query by user with conditions."""

    @abstractmethod
    def fetch(self, params: LookupConditions, user: Person) -> QueryResult:
        """Fetch by user with lockup conditions."""


class AbstractDetailExerciseRepository(ABC):
    """ABC for repository to fetch item candidates with conditions."""

    @abstractmethod
    def fetch(self, user: Person, exercise_pk: int) -> Candidates:
        """Fetch user's item candidates to study."""
