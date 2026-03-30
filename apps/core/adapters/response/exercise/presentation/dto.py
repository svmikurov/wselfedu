"""Presentation exercise case Response DTO."""

from apps.core.domains.dto import BaseDTO, ErrorField
from apps.core.domains.exercise.dto import (
    AnswerTextField,
    ExerciseStatusField,
    ProgressDataField,
    QuestionTextField,
)


class PresentationCaseResponseDTO(
    ExerciseStatusField,
    QuestionTextField,
    AnswerTextField,
    ProgressDataField,
    ErrorField,
    BaseDTO,
):
    """Presentation exercise case DTO."""
