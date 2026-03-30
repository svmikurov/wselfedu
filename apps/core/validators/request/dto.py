"""Validated data schemas."""

from pydantic import BaseModel

from apps.core.domains.dto import BaseDTO
from apps.core.domains.exercise.enums import ExerciseProcessEnum


class TestExerciseAnswerDTO(BaseDTO):
    """Test exercise answer DTO."""

    option_value: int


class ExerciseActionWebDTO(BaseModel):
    """Process exercise WEB request validated DTO."""

    action: ExerciseProcessEnum


class ProcessExerciseWebDTO(
    TestExerciseAnswerDTO,
    ExerciseActionWebDTO,
):
    """Process exercise action DTO."""
