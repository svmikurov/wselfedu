"""Type aliases for common generic."""

from typing import TypeAlias

from interfaces.protocols.domain.exercise import (
    ExerciseConfigProtocol,
)
from ports.contract.entity.domain.exercise.flow import (
    PresentationDomainResultProtocol,
)
from ports.contract.infra.domain.exercise import CreateTaskDomainProtocol

CaseAlias: TypeAlias = PresentationDomainResultProtocol

ExerciseDomainAlias: TypeAlias = CreateTaskDomainProtocol[
    ExerciseConfigProtocol,
    PresentationDomainResultProtocol,
]
