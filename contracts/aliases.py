"""Type aliases for common generic."""

from typing import TypeAlias

from contracts.entity.domain.exercise.flow import (
    PresentationDomainResultProtocol,
)
from contracts.infra.domain.exercise import CreateTaskDomainProtocol
from interfaces.protocols.domain.exercise import (
    ExerciseConfigProtocol,
)

CaseAlias: TypeAlias = PresentationDomainResultProtocol

ExerciseDomainAlias: TypeAlias = CreateTaskDomainProtocol[
    ExerciseConfigProtocol,
    PresentationDomainResultProtocol,
]
