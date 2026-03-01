"""Mathematical discipline domain DTOs."""

from typing import Literal

from pydantic import BaseModel, Field

from apps.core.domains.base_dto import BaseDTO
from apps.core.domains.exercise.enums import ExerciseStatusEnum
from apps.study.models.exercise.reward import RewardType

Operation = Literal['add', 'sub', 'mul', 'div']

# ===============================================
# Create calculation conditions
# ===============================================


class CalculationConditionDTO(BaseDTO):
    """Calculation conditions DTO."""

    min_operand: int
    max_operand: int
    operation_type: Operation


# ===============================================
# Current calculation conditions
# ===============================================


class CalculationCaseDTO(BaseModel):
    """Calculation exercise case."""

    question_text: str


class CalculationSolutionDTO(BaseModel):
    """Calculation exercise case correct solution."""

    solution_text: str


class CalculationMetaDTO(CalculationCaseDTO):
    """Calculation exercise metadata to story."""

    question_text: str
    correct_answer: int


# NOTE: It's experimental implementation
class ExerciseAvailabilityDTO(BaseModel):
    """Exercise availability DTO."""


# NOTE: It's experimental implementation
class ExerciseMilestoneDTO(BaseModel):
    """Exercise milestone DTO."""

    reward_amount: int = Field(
        description='Reward amount for success exercise completion',
    )
    reward_type: RewardType = Field(
        description='Reward type for success exercise completion',
    )


# NOTE: It's experimental implementation
class ExerciseParametersDTO(BaseModel):
    """Exercise parameters DTO."""

    conditions: CalculationConditionDTO = Field(
        description='Create exercise conditions',
    )
    availability: ExerciseAvailabilityDTO | None = Field(
        description='Exercise availability data',
        default=None,
    )
    milestone: ExerciseMilestoneDTO | None = Field(
        description='Current milestone data',
        default=None,
    )


class CalculationDataDTO(BaseDTO):
    """Calculation exercise domain result data."""

    exercise_status: ExerciseStatusEnum
    data: CalculationCaseDTO


# ===============================================
# User's answer
# ===============================================


class CalculationAnswerDTO(BaseDTO):
    """Calculation exercise user's answer."""

    user_answer: str


# ===============================================
# Regular exercise loop
# ===============================================


class CalculationLoopDTO(CalculationConditionDTO, CalculationAnswerDTO):
    """Regular calculation exercise loop DTO."""


# ===============================================
# Check user's answer result
# ===============================================


class CalculationExplainDTO(BaseDTO):
    """Calculation exercise case explain."""

    exercise_status: ExerciseStatusEnum
    data: CalculationSolutionDTO


class CalculationResultDTO(BaseDTO):
    """Calculation exercise user's answer check result."""

    is_correct: bool
