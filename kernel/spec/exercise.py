"""Exercise specification factory."""

from typing import TypeVar, override

from interfaces.protocols.domain.exercise import TestDomainResultProtocol
from interfaces.protocols.spec.exercise import (
    CheckTestSpecProtocol,
    CreateTaskSpecProtocol,
)
from interfaces.schemas.domain.exercise import TestAnswer
from interfaces.schemas.spec.exercise import CheckTestSpec
from ports.abstract.spec import AbstractExerciseSpecFactory
from ports.contract.entity.domain.exercise.fields import HasExerciseAction
from ports.interfaces.protocols.command import UserDataCommandProtocol
from ports.interfaces.schemas.domain.exercise.params import (
    ExerciseParametersDTO,
    ExerciseSpecDTO,
)
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
        CheckTestSpecProtocol,
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

    # HACK: Fix type ignore
    @override
    def create(
        self,
        command: UserDataCommandProtocol[HasExerciseAction],
        params: ExerciseParametersDTO,
        case: CaseT | None,
    ) -> CheckTestSpecProtocol:
        """Create the check answer exercise specification."""
        return CheckTestSpec(  # type: ignore
            answer=TestAnswer(
                option_value=command.data.option_value,  # type: ignore
            ),
            case=case,  # type: ignore
        )
