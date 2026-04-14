"""Exercise domain interface."""

from typing import Iterator, Protocol, Self, TypeVar, overload

from .enums import DisplayOrder, ExerciseStatusEnum

ExerciseConditionsT = TypeVar('ExerciseConditionsT')
ExerciseConfigT = TypeVar('ExerciseConfigT')
ExerciseConfig_contra = TypeVar('ExerciseConfig_contra', contravariant=True)
ExerciseSettingsT = TypeVar('ExerciseSettingsT')

OptionT = TypeVar('OptionT')
Option_co = TypeVar('Option_co', covariant=True)


class HasText(Protocol):
    """Protocol for has *text* interface."""

    text: str


# =================================================
# Exercise parameters interface
# =================================================


# Conditions
# ----------


class HasCategory(Protocol):
    """Protocol for has *category* interface."""

    category: int | None


class HasMark(Protocol):
    """Protocol for has *mark* interface."""

    mark: list[int]


class HasSource(Protocol):
    """Protocol for has *source* interface."""

    source: int | None


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


# Configuration
# -------------


class HasDisplayOrder(Protocol):
    """Protocol for item display order object interface."""

    display_order: DisplayOrder


class HasItemCount(Protocol):
    """Protocol for item count object interface."""

    item_count: int | None


class HasOptionCount(Protocol):
    """Protocol for item option count object interface."""

    option_count: int


# Settings
# --------


class HasTimeout(Protocol):
    """Protocol for exercise phase timeout interface."""

    question_timeout: int | None = None
    answer_timeout: int | None = None


# Derived interface
# -----------------


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
    HasDisplayOrder,
    HasItemCount,
    Protocol,
):
    """Protocol for exercise configuration interface."""


class ExerciseSettingsProtocol(
    HasTimeout,
    Protocol,
):
    """Protocol for exercise settings interface."""


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
# Exercise parameters DTO interface
# =================================================


class HasExerciseConditions(Protocol[ExerciseConditionsT]):
    """Protocol for has exercise conditions interface.

    Contains exercise elements select/define conditions.
    My contains:
        - database lockup conditions
        - calculation operand conditions
        - other conditions
    """

    conditions: ExerciseConditionsT


class HasExerciseConfig(Protocol[ExerciseConfigT]):
    """Protocol for has test exercise configuration interface.

    Contains display exercise configuration.
    For example:
        - question / answer timeout
        - other settings
    """

    conf: ExerciseConfigT


class HasExerciseSettings(Protocol[ExerciseSettingsT]):
    """Protocol for has exercise settings interface.

    Contains exercise display configuration, such as:
        - question / answer timeout
        - other settings
    """

    settings: ExerciseSettingsT


class GenericExerciseParameters(
    HasExerciseConditions[ExerciseConditionsT],
    HasExerciseConfig[ExerciseConfigT],
    HasExerciseSettings[ExerciseSettingsT],
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
