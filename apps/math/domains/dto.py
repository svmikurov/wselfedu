"""Mathematical discipline domain DTOs."""

from typing import Literal

from pydantic import BaseModel

from apps.core.domain.base_dto import BaseDTO
from apps.core.domain.exercise.enums import ExerciseStatusEnum

Operation = Literal['add', 'sub', 'mul', 'div']


class CalculationConditionDTO(BaseDTO):
    """Calculation conditions DTO."""

    min_operand: int
    max_operand: int
    operation_type: Operation


class CalculationCaseDTO(BaseModel):
    """Calculation exercise case."""

    question_text: str


class CalculationSolutionDTO(BaseModel):
    """Calculation exercise case solution."""

    solution_text: str


class CalculationMetaDTO(BaseModel):
    """Calculation exercise metadata to story."""

    question_text: str
    correct_answer: int
    conditions: CalculationConditionDTO


class CalculationDataDTO(BaseDTO):
    """Calculation exercise domain result data."""

    exercise_status: ExerciseStatusEnum
    data: CalculationCaseDTO


class CalculationAnswerDTO(BaseDTO):
    """Calculation exercise user's answer."""

    user_answer: str


class CalculationExplainDTO(BaseDTO):
    """Calculation exercise case explain."""

    exercise_status: ExerciseStatusEnum
    data: CalculationSolutionDTO


class CalculationResultDTO(BaseDTO):
    """Calculation exercise user's answer check result."""

    is_correct: bool
