"""Abstract base class for exercise services."""

from abc import ABC, abstractmethod

from typing_extensions import override
from wse_exercises.core.math import CalcTask

from apps.math.services.protocol import ExerciseServiceProto
from apps.math.services.types import CalcConditionType


class BaseCalcService(ExerciseServiceProto[CalcTask], ABC):
    """Abstract base class of service for creating calculation tasks."""

    @abstractmethod
    @override
    def create_task(self, data: CalcConditionType) -> CalcTask:
        """Create calculation task."""
