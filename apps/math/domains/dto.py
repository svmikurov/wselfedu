"""Mathematical discipline domain DTOs."""

from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

from apps.core.domains.base_dto import BaseDTO
from apps.core.domains.exercise.enums import ExerciseStatusEnum
from apps.study.models.exercise.availability import PeriodExecuting
from apps.study.models.exercise.reward import RewardType

Operation = Literal['add', 'sub', 'mul', 'div']


# =================================================
# Student`s exercises (assigned by mentor)
# =================================================


class StudentExerciseDTO(BaseDTO):
    """Calculation conditions DTO."""

    pk: int = Field(description='Database identifier of assigned exercise')
    name: str = Field(description='Assigned exercise name')
    mentor: str

    # Availability
    period_type: str = Field(description='Exercise period type (Daily, ...)')
    required_count: int = Field(description='Success perform for completion')
    is_active: bool
    is_completed: bool

    # Log
    success_count: int | None
    failure_count: int | None
    tracking_date: date | None

    # Reward
    reward_type: str
    reward_amount: Decimal


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

    required_count: int
    period_type: PeriodExecuting
    started_at: datetime | None = Field(
        default=None,
    )
    is_active: bool = Field(
        default=True,
    )
    is_completed: bool = Field(
        default=False,
    )
    completed_at: datetime | None = Field(
        default=None,
    )


# NOTE: It's experimental implementation
class ExerciseCompletionDTO(BaseModel):
    """Exercise completion log DTO."""

    success_count: int
    failure_count: int
    tracking_date: datetime


# NOTE: It's experimental implementation
class ExerciseRewardDTO(BaseModel):
    """Exercise reward DTO."""

    reward_amount: Decimal = Field(
        description='Reward amount for success exercise completion',
    )
    reward_type: RewardType = Field(
        description='Reward type for success exercise completion',
    )


# NOTE: It's experimental implementation
class RegularParametersDTO(BaseModel):
    """Regular exercise parameters DTO."""

    conditions: CalculationConditionDTO = Field(
        description='Create current exercise conditions',
    )


# NOTE: It's experimental implementation
class StudentParametersDTO(RegularParametersDTO):
    """Student's exercise parameters DTO."""

    availability: ExerciseAvailabilityDTO = Field(
        description='Current exercise availability data',
    )
    completion: ExerciseCompletionDTO = Field(
        description='Current exercise completion log',
    )
    reward: ExerciseRewardDTO | None = Field(
        description='Current exercise reward data',
        default=None,
    )


class CalculationDomainDTO(BaseDTO):
    """Calculation exercise domain result data."""

    exercise_status: ExerciseStatusEnum
    data: CalculationCaseDTO


class CalculationDTO(CalculationDomainDTO, StudentParametersDTO):
    """Calculation exercise data."""


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
