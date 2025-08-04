"""Defines Math app exercise service."""

from typing import Any

from wse_exercises.core import MATH_EXERCISES, MathEnum
from wse_exercises.core.math import CalcTask
from wse_exercises.core.math.base.services import OperandGeneratorABC


class CalcService:
    """Calculation exercise service.

    Creates math calculation task.
    """

    def __init__(
        self,
        operand_generator: OperandGeneratorABC,
    ) -> None:
        """Construct the services."""
        self._operand_generator = operand_generator

    def create_task(self, data: dict[str, Any]) -> CalcTask:
        """Create task."""
        exercise_name = data['exercise_name']
        exercise_type = MATH_EXERCISES[MathEnum(exercise_name)]

        print(data)

        exercise = exercise_type(
            operand_generator=self._operand_generator,
            config={
                'min_value': data['config']['min_value'],
                'max_value': data['config']['max_value'],
            },
        )

        task = exercise.create_task()
        return task
