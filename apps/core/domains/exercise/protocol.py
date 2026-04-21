"""Exercise domain interface."""

from typing import Iterator, Protocol, Self, TypeVar, overload

from apps.core.contracts import business, general
from apps.core.contracts.entity import exercise

from .enums import DisplayOrder, ExerciseProcessEnum, ExerciseStatusEnum

ExerciseConditionsT = TypeVar('ExerciseConditionsT')
ExerciseConfigT = TypeVar('ExerciseConfigT')
ExerciseConfig_contra = TypeVar('ExerciseConfig_contra', contravariant=True)
ExerciseSettingsT = TypeVar('ExerciseSettingsT')

OptionT = TypeVar('OptionT')
Option_co = TypeVar('Option_co', covariant=True)


class HasExerciseProcessAction(Protocol):
    """Protocol for has exercise process action interface."""

    action: ExerciseProcessEnum


# Derived interface
# -----------------


class ConditionsProtocol(
    business.HasCategory,
    business.HasMark,
    business.HasSource,
    business.HasPeriod,
    business.HasProgress,
    Protocol,
):
    """Protocol for exercise conditions interface."""


class ExerciseConfigProtocol(
    business.HasDisplayOrder[DisplayOrder],
    business.HasItemCount,
    Protocol,
):
    """Protocol for exercise configuration interface."""


class ExerciseSettingsProtocol(
    business.HasTimeout,
    Protocol,
):
    """Protocol for exercise settings interface."""


# =================================================
# Exercise case meta data DTO interface
# =================================================


class HasExerciseStatus(Protocol):
    """Protocol for has exercise status interface."""

    status: ExerciseStatusEnum


class HasProgressValue(Protocol):
    """Protocol for has progress value integer field."""

    progress_value: int


# =================================================
# Exercise parameters DTO interface
# =================================================


class HasCase(Protocol[OptionT]):
    """Protocol fo has *case* interface."""

    case: OptionT


class HasExistingCase(Protocol[OptionT]):
    """Protocol fo has *existing case* interface."""

    existing_case: OptionT


class GenericExerciseParameters(
    exercise.HasExerciseConditions[ExerciseConditionsT],
    exercise.HasExerciseConfig[ExerciseConfigT],
    exercise.HasExerciseSettings[ExerciseSettingsT],
    Protocol[ExerciseConditionsT, ExerciseConfigT, ExerciseSettingsT],
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
        ConditionsProtocol,
        ExerciseConfigProtocol,
        ExerciseSettingsProtocol,
    ],
    Protocol,
):
    """Exercise parameters."""


class ExerciseSpecProtocol(
    exercise.HasExerciseConditions[ConditionsProtocol],
    exercise.HasExerciseConfig[ExerciseConfigProtocol],
    exercise.HasExerciseSettings[ExerciseSettingsProtocol],
    HasExistingCase[OptionT],
    Protocol[OptionT],
):
    """Protocol for exercise spec interface."""


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
    general.HasResourceIdentifier,
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
# Exercise domain result DTO interface
# =================================================


class ExerciseProcessResultProtocol(
    HasExerciseStatus,
    HasCase[OptionT],
    Protocol,
):
    """Protocol for domain result DTO interface."""


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


# =================================================
# Exercise domain
# =================================================


class ExerciseDomainProtocol(
    Protocol[
        ExerciseConfig_contra,
        Option_co,
    ],
):
    """Protocol for exercise domain interface."""

    def execute(
        self,
        candidates: Candidates,
        conf: ExerciseConfig_contra,
    ) -> Option_co:
        """Create exercise case."""
