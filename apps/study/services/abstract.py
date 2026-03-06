"""Abstract base classes for services."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from django.db.models import Model

ExerciseAssignationModel = TypeVar('ExerciseAssignationModel', bound=Model)


class AbstractCompletionService(ABC, Generic[ExerciseAssignationModel]):
    """Assigned exercise completion service."""

    @abstractmethod
    def add_success(self, assignation_pk: int) -> None:
        """Add a successful attempt to solve the exercise."""

    @abstractmethod
    def add_failure(self, assignation_pk: int) -> None:
        """Add an unsuccessful attempt to solve the exercise."""
