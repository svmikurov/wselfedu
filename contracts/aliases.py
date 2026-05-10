"""Type aliases for common generic."""

from typing import TypeAlias

from contracts.infra.domain.exercise import CreateTaskDomainProtocol
from interfaces.protocols.domain.exercise import (
    ExerciseConfigProtocol,
)
from ports.contract.entity.domain.exercise.flow import (
    PresentationDomainResultProtocol,
)

CaseAlias: TypeAlias = PresentationDomainResultProtocol

ExerciseDomainAlias: TypeAlias = CreateTaskDomainProtocol[
    ExerciseConfigProtocol,
    PresentationDomainResultProtocol,
]
