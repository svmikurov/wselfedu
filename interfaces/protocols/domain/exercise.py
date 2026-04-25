"""General domain contracts."""

from typing import Iterator, Protocol, Self, TypeVar, overload

from interfaces.enums import exercise
from interfaces.protocols.general import HasResourceIdentifier

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


class HasExerciseStatus(Protocol):
    """Protocol for has exercise status interface."""

    status: exercise.ExerciseStatus


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


class HasAnswerText(Protocol):
    """Protocol for *exercise answer* text."""

    answer_text: str


# =================================================
# Candidate contracts for exercise task
# =================================================


class Candidate(
    HasResourceIdentifier,
    HasDefineText,
    HasMeanText,
    HasProgressValue,
    Protocol,
):
    """Protocol for a single candidate item."""

    # @property
    # def native(self) -> str: ...
    # @property
    # def foreign(self) -> str: ...
    # @property
    # def user(self) -> PersonProtocol: ...


class Candidates(Protocol[T_co]):
    """Protocol for a collection of candidates."""

    def __iter__(self) -> Iterator[T_co]:
        """Return an iterator over candidates in the collection."""
        ...

    def __len__(self) -> int:
        """Return the number of candidates in the collection."""
        ...

    @overload
    def __getitem__(self, index: int) -> T_co: ...
    @overload
    def __getitem__(self, items_slice: slice) -> Self: ...
    def __getitem__(self, index_or_slice: int | slice) -> T_co | Self:
        """Get a candidate by index or a slice of the collection."""
        ...

    def order_by(self, *field_names: str) -> Self:
        """Order the collection by one or more fields."""
        ...


CandidatesProtocol = Candidates[Candidate]
