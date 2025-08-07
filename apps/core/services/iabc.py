"""Contains protocols and abstract base classes for general services."""

from typing import Any, Protocol, TypeVar

T_cov = TypeVar('T_cov', covariant=True)


class IExerciseService(Protocol[T_cov]):
    """Protocol for task creation service interface."""

    def create_task(self, data: dict[str, Any]) -> T_cov:
        """Create task."""
