"""Protocols for exercise's domain interface."""

from typing import Protocol, TypeAlias, TypeVar

from ports.contract import enums
from ports.contract.entity.domain.exercise import (
    HasAnswerDefine,
    HasAnswerMean,
    HasAnswerText,
    HasCase,
    HasCheckResult,
    HasDefineText,
    HasDisplayOrder,
    HasExerciseKind,
    HasItem,
    HasItemCount,
    HasItems,
    HasMeanText,
    HasOptions,
    HasOptionValue,
    HasPeriod,
    HasProgress,
    HasProgressValue,
    HasQuestionDefine,
    HasQuestionMean,
    HasQuestionOptionValue,
    HasQuestionText,
    HasTimeout,
)
from ports.contract.entity.domain.general import (
    HasCategory,
    HasMark,
    HasResourceIdentifier,
    HasSource,
)
from ports.contract.entity.domain.params import (
    GenericExerciseParameters,
    HasConditions,
    HasConfig,
    HasSettings,
)
from ports.contract.entity.general import HasStatus
from ports.contract.enums import ExerciseStatus

Option_co = TypeVar('Option_co', covariant=True)


# =================================================
# Exercise parameters
# =================================================


class ConditionsProtocol(
    HasCategory,
    HasMark,
    HasSource,
    HasPeriod,
    HasProgress,
    Protocol,
):
    """Protocol for exercise conditions interface."""


class ExerciseConfigProtocol(
    HasDisplayOrder[enums.DisplayOrder],
    HasItemCount,
    Protocol,
):
    """Protocol for exercise configuration interface."""


class ExerciseSettingsProtocol(
    HasTimeout,
    Protocol,
):
    """Protocol for exercise settings interface."""


class ExerciseParametersProtocol(
    GenericExerciseParameters[
        ConditionsProtocol,
        ExerciseConfigProtocol,
        ExerciseSettingsProtocol,
    ],
    Protocol,
):
    """Exercise parameters."""


class ExerciseSpecProtocol(
    HasConditions[ConditionsProtocol],
    HasConfig[ExerciseConfigProtocol],
    HasSettings[ExerciseSettingsProtocol],
    HasCase[Option_co],
    Protocol[Option_co],
):
    """Protocol for exercise spec interface."""


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


TaskItemsT: TypeAlias = list[TaskItemProtocol]
"""Task items.
"""

# =================================================
# Task domain result
# =================================================


class PresentationDomainResultProtocol(
    HasItem[TaskItemProtocol],
    HasStatus[ExerciseStatus],
    HasExerciseKind,
    Protocol,
):
    """Protocol for presentation exercise task domain result DTO.

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
    HasItems[list[TaskItemProtocol]],
    HasStatus[ExerciseStatus],
    HasExerciseKind,
    Protocol,
):
    """Protocol for test exercise task domain result DTO.

    Parameters
    ----------
    question_option_value : `int`
        Test task item collection index of correct answer.
    items : `list[TaskItemProtocol]`
        Test task item collection for answer choice.
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
    HasQuestionText,
    HasOptions,
    Protocol,
):
    """Protocol for test exercise task interface.

    Parameters
    ----------
    question_text : `str`
        Test task question option value (list index).
    options : `list[OptionProtocol]`
        Test task options (value, text).

    """


# =================================================
# User answer
# =================================================


class TestAnswerProtocol(
    HasStatus[enums.ExerciseStatus],
    HasOptionValue,
    Protocol,
):
    """Protocol for test task answer interface.

    Parameters
    ----------
    status : `ExerciseStatus`
        Exercise status.
    option_value : `int`
        User answer test task option value.

    """


# =================================================
# Check task answer domain result
# =================================================


class CheckTestAnswerDomainResultProtocol(
    HasStatus[enums.ExerciseStatus],
    HasCheckResult,
    Protocol,
):
    """Protocol for check test answer domain result interface."""


# =================================================
# Expalain user answer domain result
# =================================================


class ExplainAnswerDomainResultProtocol(
    HasQuestionDefine,
    HasQuestionMean,
    HasAnswerDefine,
    HasAnswerMean,
    Protocol,
):
    """Protocol for explain user answer domain result interface.

    Parameters
    ----------
    question_define : `str`
        Task question definition.
    question_mean : `str`
        Task question meaning.
    answer_define : `str`
        User answer definion.
    answer_mean : `str`
        User answer meaning.

    """
