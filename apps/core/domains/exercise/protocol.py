"""Exercise domain interface."""

from typing import Protocol, TypeVar

from contracts.entity.domain import general, params
from contracts.entity.domain.exercise import fields
from contracts.enums import exercise as enums
from interfaces.protocols.domain.exercise import Candidate, Candidates

ExerciseConditionsT = TypeVar('ExerciseConditionsT')
ExerciseConfigT = TypeVar('ExerciseConfigT')
ExerciseConfig_contra = TypeVar('ExerciseConfig_contra', contravariant=True)
ExerciseSettingsT = TypeVar('ExerciseSettingsT')

CandidateT = TypeVar('CandidateT', bound=Candidate)
Case_co = TypeVar('Case_co', covariant=True)
OptionT = TypeVar('OptionT')
Option_co = TypeVar('Option_co', covariant=True)


class HasExerciseAction(Protocol):
    """Protocol for has exercise process *action* interface."""

    action: enums.ExerciseAction


# Derived interface
# -----------------


class ConditionsProtocol(
    general.HasCategory,
    general.HasMark,
    general.HasSource,
    fields.HasPeriod,
    fields.HasProgress,
    Protocol,
):
    """Protocol for exercise conditions interface."""


class ExerciseConfigProtocol(
    fields.HasDisplayOrder[enums.DisplayOrder],
    fields.HasItemCount,
    Protocol,
):
    """Protocol for exercise configuration interface."""


class ExerciseSettingsProtocol(
    fields.HasTimeout,
    Protocol,
):
    """Protocol for exercise settings interface."""


# =================================================
# Exercise parameters DTO interface
# =================================================


class HasCase(Protocol[Option_co]):
    """Protocol fo has *case* interface."""

    @property
    def case(self) -> Option_co:
        """Get case."""


class HasExistingCase(Protocol[OptionT]):
    """Protocol fo has *existing case* interface."""

    existing_case: OptionT


class GenericExerciseParameters(
    params.HasConditions[ExerciseConditionsT],
    params.HasConfig[ExerciseConfigT],
    params.HasSettings[ExerciseSettingsT],
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
    params.HasConditions[ConditionsProtocol],
    params.HasConfig[ExerciseConfigProtocol],
    params.HasSettings[ExerciseSettingsProtocol],
    HasExistingCase[OptionT],
    Protocol[OptionT],
):
    """Protocol for exercise spec interface."""


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
