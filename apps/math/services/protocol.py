"""Protocol for exercise services interface."""

from typing import Protocol, TypeVar

from apps.math.services.types import CalcConditionType

TaskT_cov = TypeVar('TaskT_cov', covariant=True)


class ExerciseServiceProto(Protocol[TaskT_cov]):
    """Protocol for task creation service interface."""

    def create_task(self, data: CalcConditionType) -> TaskT_cov:
        """Create task."""
