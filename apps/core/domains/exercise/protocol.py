"""Exercise domain interface."""

from typing import Iterator, Protocol, Self, TypeVar, overload

from .enums import DisplayOrder, ExerciseStatusEnum

ExerciseConditions = TypeVar('ExerciseConditions')
ExerciseTypeConfig = TypeVar('ExerciseTypeConfig')
ExerciseSettings = TypeVar('ExerciseSettings')
Configuration_contra = TypeVar('Configuration_contra', contravariant=True)

CandidatesT = TypeVar('CandidatesT')

# =================================================
# Exercise parameters DTO interface
# =================================================


class HasExerciseConditions(Protocol[ExerciseConditions]):
    """Protocol for has exercise conditions interface."""

    conditions: ExerciseConditions


class HasExerciseConfig(Protocol[ExerciseTypeConfig]):
    """Protocol for has test exercise configuration interface."""

    conf: ExerciseTypeConfig


class HasExerciseSettings(Protocol[ExerciseSettings]):
    """Protocol for has exercise settings interface."""

    settings: ExerciseSettings


class ExerciseParameters(
    HasExerciseConditions[ExerciseConditions],
    HasExerciseConfig[ExerciseTypeConfig],
    HasExerciseSettings[ExerciseSettings],
    Protocol[ExerciseConditions, ExerciseTypeConfig, ExerciseSettings],
):
    """Exercise parameters.

    Parameters
    ----------
    conditions :
        Study resource lockup conditions.
    conf :
        Exercise type domain configuration.
    settings :
        Exercise type perform settings.

    """


# =================================================
# Exercise type dependencies DTO interface
# =================================================


class HasItemCount(Protocol):
    """Protocol for item count object interface."""

    item_count: int


class HasDisplayOrder(Protocol):
    """Protocol for item display order object interface."""

    display_order: DisplayOrder


class HasText(Protocol):
    """Protocol for has *text* interface."""

    text: str


# =================================================
# Exercise case meta data DTO interface
# =================================================


class HasResourceIdentifier(Protocol):
    """Protocol for has resource identifier object interface."""

    pk: int


class HasExerciseStatus(Protocol):
    """Protocol for has exercise status interface."""

    exercise_status: ExerciseStatusEnum


class HasProgressValue(Protocol):
    """Protocol for has progress value integer field."""

    progress: int


# =================================================
# Exercise candidates interface
# =================================================


class HasDefineText(Protocol):
    """Protocol for exercise *define* text."""

    define: str


class HasExplainText(Protocol):
    """Protocol for exercise *explain* text."""

    explain: str


class Candidate(
    HasResourceIdentifier,
    HasDefineText,
    HasExplainText,
    HasProgressValue,
    Protocol,
):
    """Protocol for a single candidate item."""


class Candidates(Protocol):
    """Protocol for a collection of candidates."""

    def __iter__(self) -> Iterator[Candidate]:
        """Return an iterator over candidates in the collection."""
        ...

    def __len__(self) -> int:
        """Return the number of candidates in the collection."""
        ...

    @overload
    def __getitem__(self, index: int) -> Candidate: ...
    @overload
    def __getitem__(self, items_slice: slice) -> Self: ...
    def __getitem__(self, index_or_slice: int | slice) -> Candidate | Self:
        """Get a candidate by index or a slice of the collection."""
        ...

    def order_by(self, *field_names: str) -> Self:
        """Order the collection by one or more fields."""
        ...


class SelectorProtocol(Protocol[Configuration_contra]):
    """Protocol for exercise data selector interface."""

    def select(
        self,
        candidates: Candidates,
        conf: Configuration_contra,
    ) -> Candidates:
        """Select data for exercise."""


# =================================================
# Exercise case DTO interface
# =================================================


class HasQuestionText(Protocol):
    """Protocol for *exercise question* text."""

    question_text: str


class HasAnswerText(Protocol):
    """Protocol for *exercise answer* text."""

    answer_text: str


# =================================================
# Exercise check DTO interface
# =================================================


class HasUserAnswer(Protocol):
    """Protocol for *user answer* text."""

    user_answer: str


class HasCheckResult(Protocol):
    """User answer check result."""

    is_correct: bool
