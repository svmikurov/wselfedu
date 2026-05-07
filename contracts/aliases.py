"""Type aliases for common generic."""

from typing import TypeAlias

from apps.core.domains.exercise.protocol import (
    ExerciseConfigProtocol,
    ExerciseDomainProtocol,
)
from contracts.entity.domain.exercise.flow import (
    PresentationDomainResultProtocol,
)

CaseAlias: TypeAlias = PresentationDomainResultProtocol

ExerciseDomainAlias: TypeAlias = ExerciseDomainProtocol[
    ExerciseConfigProtocol,
    PresentationDomainResultProtocol,
]
