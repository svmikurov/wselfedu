"""Service interfaces."""

from typing import Protocol

from wse_exercises.core.mathem import Exercises
from wse_exercises.core.mathem.task import SimpleMathTask


class ISimpleMathExerciseService(Protocol):
    """Interface for simple exercise service."""

    def create_task(
        self,
        exercise_name: Exercises,
        conditions: dict[str, int],
    ) -> SimpleMathTask:
        """Create simple matn calculation task."""
