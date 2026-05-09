"""Exercise specification factory."""

from typing import TypeVar, override

from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.protocol import HasExerciseAction
from apps.core.factories.abstract import AbstractExerciseSpecFactory
from contracts.schemas.domain.exercise.params import (
    ExerciseParametersDTO,
    ExerciseSpecDTO,
)
from interfaces.protocols.domain.exercise import TestDomainResultProtocol
from interfaces.protocols.spec.exercise import CreateTaskSpecProtocol
from utils.audit.base import BaseAuditable
from utils.audit.protocol import AuditorProtocol

CaseT = TypeVar('CaseT')


class CreateExerciseSpecFactory(
    BaseAuditable,
    AbstractExerciseSpecFactory[
        UserDataCommandProtocol[HasExerciseAction],
        ExerciseParametersDTO,
        TestDomainResultProtocol | None,
        CreateTaskSpecProtocol,
    ],
):
    """Create task the specification factory."""

    def __init__(
        self,
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the factory."""
        super().__init__(name=name, auditor=auditor)

    @override
    def create(
        self,
        command: UserDataCommandProtocol[HasExerciseAction],
        params: ExerciseParametersDTO,
        case: TestDomainResultProtocol | None,
    ) -> CreateTaskSpecProtocol:
        """Create the create task exercise specification."""
        return ExerciseSpecDTO(
            conditions=params.conditions,
            conf=params.conf,
            settings=params.settings,
            case=case,
        )


class CheckAnswerSpecFactory(
    BaseAuditable,
    AbstractExerciseSpecFactory[
        UserDataCommandProtocol[HasExerciseAction],
        ExerciseParametersDTO,
        CaseT | None,
        ExerciseSpecDTO[CaseT],
    ],
):
    """Check answer the specification factory."""

    def __init__(
        self,
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the factory."""
        super().__init__(name=name, auditor=auditor)

    @override
    def create(
        self,
        command: UserDataCommandProtocol[HasExerciseAction],
        params: ExerciseParametersDTO,
        existing_case: CaseT | None,
    ) -> ExerciseSpecDTO[CaseT]:
        """Create the check answer exercise specification."""
        return ExerciseSpecDTO(
            conditions=params.conditions,
            conf=params.conf,
            settings=params.settings,
            case=existing_case,
        )
