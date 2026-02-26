"""Abstract base classes fot core repository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from apps.core.domains.exercise.types import (
        Candidates,
        Conditions,
        Parameters,
    )
    from apps.users.models import Person

__all__ = [
    'AbstractParametersRepository',
    'AbstractConditionsExerciseRepository',
]

T = TypeVar('T')


class AbstractParametersRepository(ABC):
    """Abstract base class for exercise parameters repository."""

    @abstractmethod
    def fetch(self, user: Person) -> Parameters:
        """Fetch user's regular exercise parameters."""


class AbstractExerciseRepository(ABC):
    """ABC for repository to fetch item candidates to study."""

    @abstractmethod
    def fetch(self, user: Person) -> Candidates:
        """Fetch user's item candidates to study."""


class AbstractConditionsExerciseRepository(ABC):
    """ABC for repository to fetch item candidates with conditions."""

    @abstractmethod
    def fetch(self, user: Person, conditions: Conditions) -> Candidates:
        """Fetch user's item candidates to study."""


class AbstractDetailExerciseRepository(ABC):
    """ABC for repository to fetch item candidates with conditions."""

    @abstractmethod
    def fetch(self, user: Person, exercise_pk: int) -> Candidates:
        """Fetch user's item candidates to study."""
