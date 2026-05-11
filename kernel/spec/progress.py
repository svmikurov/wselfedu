"""Update study progress specification factory."""

from typing import TypeVar, override

from ports.abstract.spec import AbstractExerciseSpecFactory
from ports.contract.entity.domain.exercise.fields import HasExerciseAction
from ports.interfaces.protocols.command.assembler import (
    UserDataCommandProtocol,
)
from ports.interfaces.protocols.domain import PresentationDomainResultProtocol
from ports.interfaces.protocols.repository import (
    ProgressUpdateConditionsProtocol,
)
from ports.interfaces.schemas.domain.exercise.params import (
    ExerciseParametersDTO,
)
from ports.interfaces.schemas.repository import ProgressUpdateConditions
from utils.audit import AuditorProtocol, BaseAuditable

CaseT = TypeVar('CaseT', bound=PresentationDomainResultProtocol)


class UpdateProgressSpecFactory(
    BaseAuditable,
    AbstractExerciseSpecFactory[
        UserDataCommandProtocol[HasExerciseAction],
        ExerciseParametersDTO,
        CaseT | None,
        ProgressUpdateConditionsProtocol,
    ],
):
    """Update study progress specification factory."""

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
        case: CaseT | None,
    ) -> ProgressUpdateConditionsProtocol:
        """Cerate the update study progress specification."""
        if case is None:
            raise ValueError(
                'No existing (stored) exercise. '
                'Not available update progress without exercise case.'
            )

        return ProgressUpdateConditions(
            pk=case.item.pk,
            delta=1,
        )
