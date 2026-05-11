"""Exercise configuration resolver."""

from typing import override

from interfaces.protocols.domain.exercise import ExerciseParametersProtocol
from ports.abstract.resolver import AbstractResolver
from ports.contract.entity.general import NullProtocol
from ports.contract.enums.exercise import ExerciseKind
from ports.contract.infra.repository import RepositoryProtocol
from ports.interfaces.protocols.command import UserCommandProtocol
from ports.interfaces.schemas.base import NullDTO
from utils.audit.base import BaseAuditable
from utils.audit.protocol import AuditorProtocol


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
        parameters_repository: RepositoryProtocol[
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
                params = self._repository.fetch(command.user, NullDTO())

            case _ as unexpected:
                raise ValueError(f'Got unexpected exercise type: {unexpected}')

        return params
