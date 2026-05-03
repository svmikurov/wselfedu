"""Type aliases for common generic."""

from typing import TypeAlias

from apps.core.domains.exercise.protocol import (
    ExerciseConfigProtocol,
    ExerciseDomainProtocol,
)
from contracts.entity.domain.exercise.flow import (
    PresentationDomainResultProtocol,
)
from interfaces.schemas.domain.exercise import CandidateSchema

CaseAlias: TypeAlias = PresentationDomainResultProtocol
CandidatesAlias: TypeAlias = list[CandidateSchema]

ExerciseDomainAlias: TypeAlias = ExerciseDomainProtocol[
    ExerciseConfigProtocol,
    PresentationDomainResultProtocol,
]
