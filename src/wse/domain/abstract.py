"""Abstract base classes for domain layer."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ExerciseT = TypeVar('ExerciseT')


class AbstractExerciseFactory(ABC, Generic[ExerciseT]):
    """ABC for exercise factory."""

    @abstractmethod
    def create(self, session_id: str) -> ExerciseT:
        """Create an exercise."""
