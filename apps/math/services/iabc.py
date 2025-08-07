"""Defines protocol and abstract base class for exercise services."""

from abc import ABC, abstractmethod
from typing import Any

from typing_extensions import override
from wse_exercises.core.math import CalcTask

from apps.core.services.iabc import IExerciseService


class CalcServiceABC(IExerciseService[CalcTask], ABC):
    """Abstract base class of service for creating calculation tasks."""

    @abstractmethod
    @override
    def create_task(self, data: dict[str, Any]) -> CalcTask:
        """Create calculation task."""
