"""Protocols for exercise's domain interface."""

from typing import Protocol, TypeAlias, TypeVar

from apps.core.domains.exercise.protocol import (
    GenericExerciseParameters,
    HasExistingCase,
)
from contracts import enums
from contracts.entity.domain.exercise.fields import (
    HasAnswerText,
    HasDefineText,
    HasDisplayOrder,
    HasExerciseKind,
    HasItemCount,
    HasMeanText,
    HasOptionValue,
    HasPeriod,
    HasProgress,
    HasProgressValue,
    HasQuestionOptionValue,
    HasQuestionText,
    HasTaskItem,
    HasTaskItems,
    HasTimeout,
)
from contracts.entity.domain.general import (
    HasCategory,
    HasMark,
    HasResourceIdentifier,
    HasSource,
)
from contracts.entity.domain.params import (
    HasConditions,
    HasConfig,
    HasSettings,
)
from contracts.entity.general import HasStatus
from contracts.enums import ExerciseStatus
from interfaces.schemas.web.task import Option

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
    HasExistingCase[Option_co],
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
    HasTaskItems[list[TaskItemProtocol]],
    HasStatus[ExerciseStatus],
    HasExerciseKind,
    Protocol,
):
    """Protocol for test exercise domain result DTO.

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


# =================================================
# User answer
# =================================================


class TestAnswerProtocol(
    HasOptionValue,
    Protocol,
):
    """Protocol for test task answer interface.

    Parameters
    ----------
    option_value : `int`
        User answer test task option value.

    """
