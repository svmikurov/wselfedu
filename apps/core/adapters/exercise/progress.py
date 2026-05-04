"""Exercise progress command adapter."""

from typing import TypeVar, override

from apps.core.adapters.exercise.abstract import AbstractExerciseProcessAdapter
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.protocol import HasExerciseAction
from contracts.schemas.domain.exercise.params import ExerciseParametersDTO
from interfaces.protocols.domain.exercise import Candidate
from interfaces.protocols.repository import ProgressUpdateConditionsProtocol
from interfaces.schemas.repository import ProgressUpdateConditions
from utils.audit import AuditorProtocol, BaseAuditable

CaseT = TypeVar('CaseT', bound=Candidate)


class ExerciseProgressAdapter(
    BaseAuditable,
    AbstractExerciseProcessAdapter[
        UserDataCommandProtocol[HasExerciseAction],
        ExerciseParametersDTO,
        CaseT | None,
        ProgressUpdateConditionsProtocol,
    ],
):
    """Exercise process command adapter."""

    def __init__(
        self,
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the adapter."""
        super().__init__(name=name, auditor=auditor)

    @override
    def adapt(
        self,
        command: UserDataCommandProtocol[HasExerciseAction],
        params: ExerciseParametersDTO,
        case: CaseT | None,
    ) -> ProgressUpdateConditionsProtocol:
        """Adapt exercise request data for exercise service spec."""
        if case is None:
            raise ValueError(
                'No existing (stored) exercise. '
                'Not available update progress without exercise case.'
            )

        return ProgressUpdateConditions(
            pk=case.pk,
            delta=1,
        )
