"""Test exercise case Response DTO."""

from typing import TypeVar

from interfaces.schemas.base import BaseDTO, ErrorField
from interfaces.schemas.domain.exercise.fields import (
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
