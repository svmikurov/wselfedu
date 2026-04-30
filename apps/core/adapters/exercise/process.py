"""Exercise process adapter."""

from typing import TypeVar, override

from apps.core.adapters.exercise.abstract import AbstractExerciseProcessAdapter
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.protocol import (
    HasExerciseAction,
)
from contracts.schemas.domain.exercise.params import (
    ExerciseParametersDTO,
    ExerciseSpecDTO,
)

CaseT = TypeVar('CaseT')


class ExerciseProcessAdapter(
    AbstractExerciseProcessAdapter[
        UserDataCommandProtocol[HasExerciseAction],
        ExerciseParametersDTO,
        CaseT | None,
        ExerciseSpecDTO[CaseT],
    ],
):
    """Exercise process adapter."""

    @override
    def adapt(
        self,
        command: UserDataCommandProtocol[HasExerciseAction],
        params: ExerciseParametersDTO,
        existing_case: CaseT | None,
    ) -> ExerciseSpecDTO[CaseT]:
        """Adapt exercise request data for exercise service spec."""
        return ExerciseSpecDTO(
            conditions=params.conditions,
            conf=params.conf,
            settings=params.settings,
            existing_case=existing_case,
        )
