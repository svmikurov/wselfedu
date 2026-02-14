"""Mathematical discipline domain DTOs."""

from typing import Literal

from pydantic import BaseModel

from apps.core.domain.base_dto import BaseDTO
from apps.core.domain.exercise.enums import ExerciseStatusEnum

Operation = Literal['add', 'sub', 'mul', 'div']


class CalculationConditions(BaseDTO):
    """Calculation conditions DTO."""

    min_operand: str
    max_operand: str
    operation_type: Operation


class CalculationCase(BaseModel):
    """Calculation exercise case."""

    question_text: str


class CalculationSolution(BaseModel):
    """Calculation exercise case solution."""

    solution_text: str


class CalculationMeta(BaseModel):
    """Calculation exercise metadata to story."""

    question_text: str
    correct_answer: int
    conditions: CalculationConditions


class CalculationData(BaseDTO):
    """Calculation exercise domain result data."""

    exercise_status: ExerciseStatusEnum
    data: CalculationCase


class CalculationAnswer(BaseDTO):
    """Calculation exercise user's answer."""

    user_answer: str


class CalculationExplain(BaseDTO):
    """Calculation exercise case explain."""

    exercise_status: ExerciseStatusEnum
    data: CalculationSolution


class CalculationResult(BaseDTO):
    """Calculation exercise user's answer check result."""

    is_correct: bool
