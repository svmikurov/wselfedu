"""Validated data schemas."""

from apps.core.domains.dto import BaseDTO
from apps.core.domains.exercise.enums import ExerciseProcessEnum


class TestExerciseAnswerDTO(BaseDTO):
    """Test exercise answer DTO."""

    option_value: int


class ExerciseActionWebDTO(BaseDTO):
    """Process exercise WEB request validated DTO."""

    action: ExerciseProcessEnum


class ProcessExerciseWebDTO(
    TestExerciseAnswerDTO,
    ExerciseActionWebDTO,
):
    """Process exercise action DTO."""
