"""Abstract base classes for services."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from django.db.models import Model

if TYPE_CHECKING:
    from apps.math.domains.dto import (
        ExerciseAvailabilityDTO,
        ExerciseCompletionDTO,
    )

ExerciseAssignationModel = TypeVar('ExerciseAssignationModel', bound=Model)


class AbstractCompletionService(ABC, Generic[ExerciseAssignationModel]):
    """Assigned exercise completion service."""

    @abstractmethod
    def add_success(
        self,
        assignation_pk: int,
        availability: ExerciseAvailabilityDTO,
        completion: ExerciseCompletionDTO,
    ) -> bool:
        """Add a successful attempt to solve the exercise."""

    @abstractmethod
    def add_failure(self, assignation_pk: int) -> None:
        """Add an unsuccessful attempt to solve the exercise."""
