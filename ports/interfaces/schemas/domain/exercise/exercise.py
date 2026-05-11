"""Exercise's domain schema interfaces."""

from pydantic import ConfigDict

from ports.contract import enums
from ports.interfaces.schemas.base import ArbitraryDTO
from ports.interfaces.schemas.domain.exercise.fields import (
    DefineField,
    IsCorrectAnswerField,
    MeanField,
    OptionValueField,
    ProgressValueField,
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
# Exercise domain result
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
# Task answer check result
# =================================================


class TestAnswer(OptionValueField):
    """Test answer schema.

    Parameters
    ----------
    option_value : `int`
        User answer test task option value.

    """

    __test__ = False


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
