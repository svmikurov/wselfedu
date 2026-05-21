"""Exercise's domain schema interfaces."""

from pydantic import ConfigDict

from ports.contract import enums
from ports.interfaces.schemas.base import ArbitraryDTO
from ports.interfaces.schemas.domain.exercise.fields import (
    AnswerDefineField,
    AnswerMeanField,
    DefineField,
    IsCorrectAnswerField,
    MeanField,
    OptionValueField,
    ProgressValueField,
    QuestionDefineField,
    QuestionMeanField,
)
from ports.interfaces.schemas.fields import (
    ResourceIdentifierField,
    StatusField,
)

# =================================================
# Task
# =================================================


class TaskItem(
    ResourceIdentifierField,
    DefineField,
    MeanField,
    ProgressValueField,
):
    """Exercise task item schema.

    Parameters
    ----------
    pk : `int`
        Task item database indentifier.
    define : `str`
        Task item definition.
    mean : `str`
        Task item meaning.
    progress_value : `int`
        Item study integer progress value.

    """

    model_config = ConfigDict(  # type: ignore
        extra='forbid',
        frozen=True,
        from_attributes=True,
    )


# =================================================
# Create task domain result
# =================================================


class PresentationTaskDomainResult(ArbitraryDTO):
    """Presentation task domain result DTO."""

    item: TaskItem
    status: enums.ExerciseStatus
    exercise_kind: enums.ExerciseKind = enums.ExerciseKind.PRESENTATION


class TestTaskDomainResult(ArbitraryDTO):
    """Test task domain result DTO."""

    __test__ = False

    question_option_value: int
    items: list[TaskItem]
    status: enums.ExerciseStatus
    exercise_kind: enums.ExerciseKind = enums.ExerciseKind.TEST


# =================================================
# User answer
# =================================================


class TestAnswer(OptionValueField):
    """Test answer schema.

    Parameters
    ----------
    option_value : `int`
        User answer test task option value.

    """

    __test__ = False


# =================================================
# Check answer
# =================================================


class CheckTaskResult(
    StatusField[enums.ExerciseStatus],
    IsCorrectAnswerField,
):
    """Check task result schema.

    Parameters
    ----------
    status : `ExerciseStatus`
        Exercise status.
    is_correct : `bool`
        User task answer check result.

    """


# =================================================
# Test task user answer explain
# =================================================


class ExplainTaskResult(
    QuestionDefineField,
    QuestionMeanField,
    AnswerDefineField,
    AnswerMeanField,
):
    """Test task user answer explain domain result schema.

    Parameters
    ----------
    question_define : `str`
        Task question definition.
    question_mean : `str`
        Task question meaning.
    answer_define : `str`
        User answer option definition.
    answer_mean : `str`
        User answer option meaning.

    """
