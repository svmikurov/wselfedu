"""Presentation exercise case Response DTO."""

from apps.core.domains.dto import BaseDTO, ErrorField
from apps.core.domains.exercise.dto import (
    AnswerTextField,
    ExerciseStatusSchema,
    ProgressDataField,
    QuestionTextField,
)


class PresentationCaseWebResponseDTO(
    ExerciseStatusSchema,
    QuestionTextField,
    AnswerTextField,
    ProgressDataField,
    ErrorField,
    BaseDTO,
):
    """Presentation exercise case DTO."""
