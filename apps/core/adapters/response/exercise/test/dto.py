"""Test exercise case Response DTO."""

from typing import TypeVar

from contracts.schemas.base import BaseDTO, ErrorField
from contracts.schemas.domain.exercise.fields import (
    AnswerTextField,
    ExerciseStatusField,
    ProgressDataField,
    QuestionTextField,
)

ProgressT = TypeVar('ProgressT')


class TestExerciseCaseResponseDTO(
    ExerciseStatusField,
    QuestionTextField,
    AnswerTextField,
    ProgressDataField[ProgressT],
    ErrorField,
    BaseDTO,
):
    """Presentation exercise case DTO."""
