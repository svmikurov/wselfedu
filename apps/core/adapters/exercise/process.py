"""Exercise specification factory."""

from typing import TypeVar, override

from apps.core.adapters.exercise.abstract import AbstractExerciseSpecFactory
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.protocol import (
    HasExerciseAction,
)
from contracts.schemas.domain.exercise.params import (
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
        CaseT | None,
        ExerciseSpecDTO[CaseT],
    ],
):
    """Exercise specification factory."""

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
        """Create the exercise specification."""
        return ExerciseSpecDTO(
            conditions=params.conditions,
            conf=params.conf,
            settings=params.settings,
            existing_case=existing_case,
        )
