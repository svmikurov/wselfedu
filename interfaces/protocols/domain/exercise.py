"""Protocols for exercise's domain interface."""

from typing import Protocol

from contracts.entity.domain.exercise.fields import (
    HasAnswerText,
    HasExerciseDomainOptions,
    HasProgressValue,
    HasQuestionOptionValue,
    HasQuestionText,
)

# =================================================
# Exercise task
# =================================================


class PresentationTaskProtocol(
    HasQuestionText,
    HasAnswerText,
    HasProgressValue,
    Protocol,
):
    """Protocol for presentation exercise task interface."""


class TestTaskProtocol(
    HasQuestionOptionValue,
    HasExerciseDomainOptions,
    Protocol,
):
    """Protocol for test exercise task interface."""
