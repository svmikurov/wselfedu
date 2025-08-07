"""Defines Math app exercise service."""

from typing import Any

from typing_extensions import override
from wse_exercises.core import MATH_EXERCISES, MathEnum
from wse_exercises.core.math import CalcTask
from wse_exercises.core.math.base.services import OperandGeneratorABC

from apps.math.services.iabc import CalcServiceABC


class CalcService(CalcServiceABC):
    """Service for creating calculation tasks.

    Creates math calculation task.
    """

    def __init__(
        self,
        operand_generator: OperandGeneratorABC,
    ) -> None:
        """Construct the services."""
        self._operand_generator = operand_generator

    @override
    def create_task(self, data: dict[str, Any]) -> CalcTask:
        """Create calculation task."""
        exercise_name = data['exercise_name']
        exercise_type = MATH_EXERCISES[MathEnum(exercise_name)]

        exercise = exercise_type(
            operand_generator=self._operand_generator,
            config={
                'min_value': data['config']['min_value'],
                'max_value': data['config']['max_value'],
            },
        )

        task = exercise.create_task()
        return task
