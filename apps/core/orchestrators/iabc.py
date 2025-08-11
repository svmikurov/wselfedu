"""Defines protocols and ABC for orchestrator interface."""

from typing import Any, Protocol

from apps.users.models import ExerciseAssigned


class IExerciseAssignator(Protocol):
    """Protocol for exercise model management service interface."""

    def create(self, data: dict[str, Any]) -> ExerciseAssigned:
        """Assign an exercise."""

    @staticmethod
    def delete(exercise_id: int) -> None:
        """Delete the exercise from assigned exercises."""
