"""Exercise domain interface."""

from typing import Iterator, Protocol, Self, TypeVar, overload

from .enums import DisplayOrder, ExerciseStatusEnum

ExerciseConditionsT = TypeVar('ExerciseConditionsT')
ExerciseTypeConfigT = TypeVar('ExerciseTypeConfigT')
ExerciseSettingsT = TypeVar('ExerciseSettingsT')

CandidatesT = TypeVar('CandidatesT')
OptionT = TypeVar('OptionT')

# =================================================
# Exercise parameters DTO interface
# =================================================


class ExerciseConditions(Protocol):
    """Exercise conditions DTO interface."""


class ExerciseConfig(Protocol):
    """Exercise domain configuration DTO interface."""


class ExerciseSettings(Protocol):
    """Exercise perform setting DTO interface."""


class HasExerciseConditions(Protocol[ExerciseConditionsT]):
    """Protocol for has exercise conditions interface."""

    conditions: ExerciseConditionsT


class HasExerciseConfig(Protocol[ExerciseTypeConfigT]):
    """Protocol for has test exercise configuration interface."""

    conf: ExerciseTypeConfigT


class HasExerciseSettings(Protocol[ExerciseSettingsT]):
    """Protocol for has exercise settings interface."""

    settings: ExerciseSettingsT


class GenericExerciseParameters(
    HasExerciseConditions[ExerciseConditionsT],
    HasExerciseConfig[ExerciseTypeConfigT],
    HasExerciseSettings[ExerciseSettingsT],
    Protocol[ExerciseConditionsT, ExerciseTypeConfigT, ExerciseSettingsT],
):
    """Generic exercise parameters.

    Parameters
    ----------
    conditions :
        Study resource lockup or task create conditions.
    conf :
        Exercise type domain configuration.
    settings :
        Exercise type perform settings.

    """


class ExerciseParametersProtocol(
    GenericExerciseParameters[
        ExerciseConditions,
        ExerciseConfig,
        ExerciseSettings,
    ]
):
    """Exercise parameters."""


# =================================================
# Exercise configurations, settings DTO interface
# =================================================


class HasItemCount(Protocol):
    """Protocol for item count object interface."""

    item_count: int


class HasOptionCount(Protocol):
    """Protocol for item option count object interface."""

    option_count: int


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

    status: ExerciseStatusEnum


class HasProgressValue(Protocol):
    """Protocol for has progress value integer field."""

    progress_value: int


# =================================================
# Exercise candidates interface
# =================================================


class HasDefineText(Protocol):
    """Protocol for exercise *define* text."""

    define: str


class HasMeanText(Protocol):
    """Protocol for exercise *mean* text."""

    mean: str


class Candidate(
    HasResourceIdentifier,
    HasDefineText,
    HasMeanText,
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


# =================================================
# Exercise option DTO interface
# =================================================


class HasOptionValue(Protocol):
    """Protocol for has *value* interface."""

    value: int


class HasOption(Protocol[OptionT]):
    """Protocol for has *option* interface."""

    option: OptionT


class HasOptions(Protocol[OptionT]):
    """Protocol for has *options* interface."""

    options: list[OptionT]


class HasPhases(Protocol):
    """Protocol for has *phases* interface."""

    phases: list[DisplayOrder]


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
