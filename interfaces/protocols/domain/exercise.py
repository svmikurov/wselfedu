"""Protocols for exercise's domain interface."""

from typing import Protocol

from contracts.entity.domain.exercise.fields import (
    HasAnswerText,
    HasDefineText,
    HasExerciseDomainOptions,
    HasMeanText,
    HasProgressValue,
    HasQuestionOptionValue,
    HasQuestionText,
)
from contracts.entity.domain.general import HasResourceIdentifier
from interfaces.schemas.domain.exercise import Option

# =================================================
# Exercise task
# =================================================


class Candidate(
    HasResourceIdentifier,
    HasDefineText,
    HasMeanText,
    HasProgressValue,
    Protocol,
):
    """Protocol for a single candidate item."""


Candidates = list[Candidate]


class PresentationTaskProtocol(
    HasQuestionText,
    HasAnswerText,
    HasProgressValue,
    Protocol,
):
    """Protocol for presentation exercise task interface."""


class TestTaskProtocol(
    HasQuestionOptionValue,
    HasExerciseDomainOptions[list[Option]],
    Protocol,
):
    """Protocol for test exercise task interface."""
