"""Protocols for exercise's domain interface."""

from typing import Protocol, TypeAlias

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
# Task candidates
# =================================================


class CandidateProtocol(
    HasResourceIdentifier,
    HasDefineText,
    HasMeanText,
    HasProgressValue,
    Protocol,
):
    """Protocol for a single candidate item.

    Parameters
    ----------
    pk : `int`
        Item resource database identifier.
    define : `str`
        Item definition string representation.
    mean : `str`
        Item meaning string representation.
    progress_value : `int`
        Item study progress value.

    """


CandidatesT: TypeAlias = list[CandidateProtocol]
"""Candidates for task creation.
"""


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
    """Protocol for task item.

    Parameters
    ----------
    pk : `int`
        Item resource database identifier.
    define : `str`
        Item definition string representation.
    mean : `str`
        Item meaning string representation.
    progress_value : `int`
        Item study progress value.

    """


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
    """Protocol for presentation exercise domain result DTO.

    Parameters
    ----------
    item : `TaskItemProtocol`
        Presentation task.
    status : `ExerciseStatus`
        Exercise status (e.g., new task).
    exercise_kind : `ExerciseKind`
        Exercise kind (e.g., presentation, test)

    """


class TestDomainResultProtocol(
    HasQuestionOptionValue,
    HasTaskItems[TaskItemProtocol],
    HasStatus[ExerciseStatus],
    HasExerciseKind,
    Protocol,
):
    """Protocol for test exercise domain result DTO.

    Parameters
    ----------
    question_option_value : `int`
        Test task question option value (list index).
    items : `list[Option]`
        Test task options (value, text).
    status : `ExerciseStatus`
        Exercise status (e.g., new task).
    exercise_kind : `ExerciseKind`
        Exercise kind (e.g., presentation, test)

    """


# =================================================
# Tasks
# =================================================


class PresentationTaskProtocol(
    HasQuestionText,
    HasAnswerText,
    HasProgressValue,
    Protocol,
):
    """Protocol for presentation exercise task interface.

    Parameters
    ----------
    question_text : `str`
        Task question text.
    answer_text : `str`
        Task correct answer text.
    progress_value : `int`
        Item study progress value.

    """


class TestTaskProtocol(
    HasQuestionOptionValue,
    HasTaskItems[list[Option]],
    Protocol,
):
    """Protocol for test exercise task interface.

    Parameters
    ----------
    question_option_value : `int`
        Test task question option value (list index).
    items : `list[Option]`
        Test task options (value, text).

    """
