"""Core domain exercise DTOs."""

from typing import TypeVar

from contracts.schemas.base import BaseDTO
from contracts.schemas.domain.exercise.fields import (
    AnswerTextField,
    IsCorrectAnswerField,
    QuestionTextField,
    SelectedAnswerTextField,
    SelectedQuestionTextField,
)

DomainType = TypeVar('DomainType')
DomainResult = TypeVar('DomainResult')
OptionT = TypeVar('OptionT')


# -------------------------------------------------
# Text exercise check result DTO
# -------------------------------------------------


class TextExerciseCheckResult(
    IsCorrectAnswerField,
    # QuestionTextField,
    # AnswerTextField,
    # SelectedQuestionTextField,
    # SelectedAnswerTextField,
    BaseDTO,
):
    """Explanation of the test answer option."""


# -------------------------------------------------
# Text exercise explain DTO
# -------------------------------------------------


class TextExerciseExplainDTO(
    QuestionTextField,
    AnswerTextField,
    SelectedQuestionTextField,
    SelectedAnswerTextField,
    BaseDTO,
):
    """Explanation of the test answer option."""
