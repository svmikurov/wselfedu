"""Defines mathematical application factories."""

from typing import Protocol, Type

from wse_exercises.core import MathEnum
from wse_exercises.core.math.base.exercise import SimpleCalcExercise
from wse_exercises.core.math.base.services import OperandGenerator


class IExerciseFactory(Protocol):
    """Protocol for simple calculation exercise factory interface."""

    def get(self, name: MathEnum) -> SimpleCalcExercise:
        """Get simple calculation exercise instance."""


class ExercisesFactory(IExerciseFactory):
    """Protocol for simple calculation exercise factory interface."""

    def __init__(
        self,
        exercises: dict[MathEnum, Type[SimpleCalcExercise]],
        operand_generator: OperandGenerator,
    ) -> None:
        """Construct the factory."""
        self._exercises = exercises
        self._operand_generator = operand_generator

    def get(self, name: MathEnum) -> SimpleCalcExercise:
        """Get simple calculation exercise instance."""
        exercise_type = self._exercises[name]
        return exercise_type(self._operand_generator)
