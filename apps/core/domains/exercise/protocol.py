"""Exercise domain interface."""

from typing import Protocol, TypeVar

from contracts.entity.domain import params
from contracts.entity.domain.exercise import fields
from contracts.enums import exercise as enums

ExerciseConditions_co = TypeVar('ExerciseConditions_co', covariant=True)
ExerciseConfig_co = TypeVar('ExerciseConfig_co', covariant=True)
ExerciseConfig_contra = TypeVar('ExerciseConfig_contra', contravariant=True)
ExerciseSettings_co = TypeVar('ExerciseSettings_co', covariant=True)

CandidateT = TypeVar('CandidateT')
Case_co = TypeVar('Case_co', covariant=True)
OptionT = TypeVar('OptionT')
Option_co = TypeVar('Option_co', covariant=True)


class HasExerciseAction(Protocol):
    """Protocol for has exercise process *action* interface."""

    action: enums.ExerciseAction


# =================================================
# Exercise parameters DTO interface
# =================================================


class HasCase(Protocol[Option_co]):
    """Protocol fo has *case* interface."""

    @property
    def case(self) -> Option_co:
        """Get case."""


class HasExistingCase(Protocol[Option_co]):
    """Protocol fo has *existing case* interface."""

    @property
    def existing_case(self) -> Option_co | None: ...  # noqa


class GenericExerciseParameters(
    params.HasConditions[ExerciseConditions_co],
    params.HasConfig[ExerciseConfig_co],
    params.HasSettings[ExerciseSettings_co],
    Protocol[ExerciseConditions_co, ExerciseConfig_co, ExerciseSettings_co],
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


# =================================================
# Exercise option DTO interface
# =================================================


class HasPhases(Protocol):
    """Protocol for has *phases* interface."""

    phases: list[enums.DisplayOrder]


# =================================================
# Exercise domain result DTO interface
# =================================================


class ExerciseProcessResultProtocol(
    fields.HasExerciseStatus,
    HasCase[Case_co],
    Protocol,
):
    """Protocol for domain result DTO interface."""


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
