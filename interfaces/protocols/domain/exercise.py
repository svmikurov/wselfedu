"""Protocols for exercise's domain interface."""

from typing import Protocol

from contracts.entity.domain.exercise.fields import (
    HasAnswerText,
    HasDefineText,
    HasExerciseKind,
    HasMeanText,
    HasProgressValue,
    HasQuestionOptionValue,
    HasQuestionText,
    HasTaskItem,
    HasTaskItems,
)
from contracts.entity.domain.general import HasResourceIdentifier
from contracts.entity.general import HasStatus
from contracts.enums import ExerciseStatus
from interfaces.schemas.web.task import Option

# =================================================
# Exercise candidates
# =================================================


class CandidateProtocol(
    HasResourceIdentifier,
    HasDefineText,
    HasMeanText,
    HasProgressValue,
    Protocol,
):
    """Protocol for a single candidate item."""


CandidatesProtocol = list[CandidateProtocol]


# =================================================
# Task item
# =================================================


class TaskItemProtocol(
    HasResourceIdentifier,
    HasDefineText,
    HasMeanText,
    HasProgressValue,
    Protocol,
):
    """Protocol for task item."""


TaskItemsProtocol = list[TaskItemProtocol]


# =================================================
# Exercise domain result
# =================================================


class PresentationDomainResultProtocol(
    HasTaskItem[TaskItemProtocol],
    HasStatus[ExerciseStatus],
    HasExerciseKind,
    Protocol,
):
    """Protocol for presentation exercise domain result DTO."""


class TestDomainResultProtocol(
    HasQuestionOptionValue,
    HasTaskItems[TaskItemProtocol],
    HasStatus[ExerciseStatus],
    HasExerciseKind,
    Protocol,
):
    """Protocol for test exercise domain result DTO."""


class PresentationTaskProtocol(
    HasQuestionText,
    HasAnswerText,
    HasProgressValue,
    Protocol,
):
    """Protocol for presentation exercise task interface."""


class TestTaskProtocol(
    HasQuestionOptionValue,
    HasTaskItems[list[Option]],
    Protocol,
):
    """Protocol for test exercise task interface."""
