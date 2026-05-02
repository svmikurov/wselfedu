"""Exercise configuration resolver."""

from typing import override

from apps.core.assemblers.protocol import UserCommandProtocol
from apps.core.domains.exercise.protocol import ExerciseParametersProtocol
from apps.core.repositories.protocol import UserRepositoryProtocol
from contracts.entity.general import NullProtocol
from contracts.enums.exercise import ExerciseKind
from contracts.schemas.base import NullDTO
from utils.audit.base import BaseAuditable
from utils.audit.protocol import AuditorProtocol

from ..abstract import AbstractResolver


# NOTE: Temporary simple implementation
# TODO: Add cache store
class ExerciseConfigurationResolver(
    BaseAuditable,
    AbstractResolver[
        UserCommandProtocol,
        ExerciseParametersProtocol,
    ],
):
    """Exercise configuration resolver."""

    def __init__(
        self,
        exercise_type: ExerciseKind,
        parameters_repository: UserRepositoryProtocol[
            NullProtocol,
            ExerciseParametersProtocol,
        ],
        default: ExerciseParametersProtocol | None = None,
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the resolver."""
        super().__init__(name=name, auditor=auditor)
        self._exercise_type = exercise_type
        self._repository = parameters_repository
        self._default = default

    @override
    def resolve(
        self,
        command: UserCommandProtocol,
    ) -> ExerciseParametersProtocol:
        """Get exercise configuration."""
        match self._exercise_type:
            case ExerciseKind.PRESENTATION:
                params = self._repository.fetch(command.user, NullDTO())

            case ExerciseKind.TEST:
                if not self._default:
                    raise AttributeError('Define default exercise config')
                params = self._default

            case _ as unexpected:
                raise ValueError(f'Got unexpected exercise type: {unexpected}')

        return params
