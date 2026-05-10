"""General domain contracts."""

from typing import Protocol, TypeVar

from ports.contract import enums
from ports.contract.entity import general

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)

CaseT = TypeVar('CaseT')
DomainT = TypeVar('DomainT')
Case_co = TypeVar('Case_co', covariant=True)
ExceptionT = TypeVar('ExceptionT')


class HasExerciseAction(Protocol):
    """Protocol for has exercise process *action* interface."""

    action: enums.ExerciseAction


# =================================================
# Exercise kind
# =================================================


class HasExerciseKind(Protocol):
    """Protocol for has *exercise_kind* interface."""

    exercise_kind: enums.ExerciseKind


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


class HasItem(Protocol[T]):
    """Protocol for has *item* DTO interface."""

    item: T


class HasOption(Protocol[T]):
    """Protocol for has *option* DTO interface."""

    option: T


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


class HasExerciseStatus(
    general.HasStatus[enums.ExerciseStatus],
    Protocol,
):
    """Protocol for has exercise status interface."""

    status: enums.ExerciseStatus


# =================================================
# Exercise component contracts
# =================================================


class HasDefineText(Protocol):
    """Protocol for exercise *define* text."""

    define: str


class HasMeanText(Protocol):
    """Protocol for exercise *mean* text."""

    mean: str


class HasQuestionText(Protocol):
    """Protocol for *exercise question* text."""

    question_text: str


class HasAnswer(Protocol[T_co]):
    """Protocol for *answer* DTO's field."""

    @property
    def answer(self) -> T_co: ...  # noqa


class HasAnswerText(Protocol):
    """Protocol for *exercise answer* text."""

    answer_text: str


# =================================================
# Exercise answer
# =================================================


class HasOptionValue(Protocol):
    """Protocol for has *option_value* DTO field."""

    option_value: int


# =================================================
# Exercise domain result / failure DTO's interface
# =================================================


class HasCase(Protocol[Case_co]):
    """Protocol fo has *case* interface."""

    @property
    def case(self) -> Case_co | None: ...  # noqa


class HasDomain(Protocol[DomainT]):
    """Protocol fo has *domain* interface."""

    domain: DomainT


class ExerciseCaseProtocol(
    HasExerciseStatus,
    HasDomain[DomainT],
    Protocol,
):
    """Protocol for exercise case DTO interface."""


class HasQuestionOptionValue(Protocol):
    """Protocol for has question *option_value* interface."""

    question_option_value: int


class HasTaskItem(Protocol[T]):
    """Protocol for has task *item* interface."""

    item: T


class HasTaskItems(Protocol[T]):
    """Protocol for has task *items* interface."""

    items: T


# =================================================
# User answer
# =================================================


# =================================================
# Check user answer
# =================================================
