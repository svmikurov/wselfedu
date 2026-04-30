"""Type aliases for common generic."""

from typing import TypeAlias

from apps.core.domains.exercise.protocol import (
    ExerciseConfigProtocol,
    ExerciseDomainProtocol,
)
from contracts.entity.domain.exercise.flow import (
    PresentationDomainResultProtocol,
)

from .entity.domain.exercise.fields import Candidates

CaseAlias: TypeAlias = PresentationDomainResultProtocol
CandidatesAlias: TypeAlias = Candidates

ExerciseDomainAlias: TypeAlias = ExerciseDomainProtocol[
    ExerciseConfigProtocol,
    CaseAlias,
]
