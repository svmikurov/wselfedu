"""Contracts for exercise domain."""

from typing import Protocol, TypeVar
from ports.contract.enums import ExerciseAction, ExerciseKind, ExerciseStatus
from ports.contract.entity.domain.general import HasText, HasValue
from ports.contract.entity.general import HasStatus

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)


# =================================================
# Conditions
# =================================================


class HasPeriod(Protocol):
    """Protocol for has *start_period*, *end_period* interface."""

    start_period: int | None
    end_period: int | None


class HasProgress(Protocol):
    """Protocol for has progress interface."""

    is_study: bool = True
    is_repeat: bool = True
    is_examine: bool = True
    is_know: bool = True


class HasProgressValue(Protocol):
    """Protocol for has progress value integer field."""

    progress_value: int


# =================================================
# Configuration
# =================================================


class HasDisplayOrder(Protocol[T]):
    """Protocol for item display order object interface."""

    display_order: T


class HasItemCount(Protocol):
    """Protocol for item count object interface."""

    item_count: int | None


class HasOptionCount(Protocol):
    """Protocol for item option count object interface."""

    option_count: int


# =================================================
# Settings
# =================================================


class HasTimeout(Protocol):
    """Protocol for exercise phase timeout interface."""

    question_timeout: int | None = None
    answer_timeout: int | None = None


# =================================================
# Task candidate fields
# =================================================


class HasDefineText(Protocol):
    """Protocol for exercise *define* text DTO field."""

    define: str


class HasMeanText(Protocol):
    """Protocol for exercise *mean* text DTO field."""

    mean: str


# =================================================
# Task fields
# =================================================


class HasQuestionText(Protocol):
    """Protocol for *question_text* DTO field."""

    question_text: str


class HasAnswerText(Protocol):
    """Protocol for *answer_text* DTO field."""

    answer_text: str


class HasQuestionOptionValue(Protocol):
    """Protocol for has *question_option_value* DTO field."""

    question_option_value: int


class HasOptionValue(Protocol):
    """Protocol for has *option_value* DTO field."""

    option_value: int


class HasItem(Protocol[T_co]):
    """Protocol for has *item* DTO field."""

    @property
    def item(self) -> T_co:
        """Item."""


class HasItems(Protocol[T_co]):
    """Protocol for has *items* DTO field."""

    @property
    def items(self) -> T_co:
        """Task items."""


# =================================================
# Task meta
# =================================================


class HasExerciseAction(Protocol):
    """Protocol for has exercise process *action* DTO field."""

    action: ExerciseAction


class HasExerciseKind(Protocol):
    """Protocol for has *exercise_kind* DTO field."""

    exercise_kind: ExerciseKind


class HasExerciseStatus(
    HasStatus[ExerciseStatus],
    Protocol,
):
    """Protocol for has exercise status interface."""


# =================================================
# Task wrap
# =================================================


class OptionProtocol(
    HasValue,
    HasText,
    Protocol,
):
    """Protocol for response context test task option representation.

    Parameters
    ----------
    value : `int`
        Task option enumeration value.
    text : `str`
        Task option text.

    """


class HasOption(Protocol):
    """Protocol for has *option* DTO field."""

    option: OptionProtocol


class HasOptions(Protocol):
    """Protocol for has *options* DTO DTO field."""

    options: list[OptionProtocol]


class HasDomain(Protocol[T]):
    """Protocol fo has *domain* DTO field."""

    domain: T


class HasTask(Protocol[T]):
    """Protocol for has *task* DTO field."""

    task: T


class HasCase(Protocol[T_co]):
    """Protocol fo has *case* DTO field."""

    @property
    def case(self) -> T_co | None: ...  # noqa


# =================================================
# Answer
# =================================================


class HasAnswer(Protocol[T_co]):
    """Protocol for *answer* DTO's field."""

    @property
    def answer(self) -> T_co: ...  # noqa


# =================================================
# Answer check
# =================================================


class HasCheckResult(Protocol):
    """User answer check result."""

    is_correct: bool