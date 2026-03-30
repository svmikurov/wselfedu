"""Exercise configuration resolver."""

from apps.core.assemblers.protocol import UserCommandProtocol
from apps.core.domains.exercise.dto import ExerciseParametersDTO
from apps.core.domains.exercise.enums import ExerciseTypeEnum
from apps.core.domains.null import NullDTO
from apps.core.repositories.protocol import UserRepositoryProtocol

from ..abstract import AbstractExerciseConfigurationResolver


# NOTE: Temporary simple implementation
# TODO: Add cache store
class ExerciseConfigurationResolver(
    AbstractExerciseConfigurationResolver[
        UserCommandProtocol,
        ExerciseParametersDTO,
    ],
):
    """Exercise configuration resolver."""

    def __init__(
        self,
        exercise_type: ExerciseTypeEnum,
        parameters_repository: UserRepositoryProtocol[
            NullDTO,
            ExerciseParametersDTO,
        ],
        default: ExerciseParametersDTO | None = None,
    ) -> None:
        """Construct the resolver."""
        self._exercise_type = exercise_type
        self._repository = parameters_repository
        self._default = default

    def resolve(
        self,
        command: UserCommandProtocol,
    ) -> ExerciseParametersDTO:
        """Get exercise configuration."""
        match self._exercise_type:
            case ExerciseTypeEnum.PRESENTATION:
                return self._repository.fetch(command.user, NullDTO())

            case ExerciseTypeEnum.TEST:
                if not self._default:
                    raise AttributeError('Define default exercise config')
                return self._default

            case _ as unexpected:
                raise ValueError(f'Got unexpected exercise type: {unexpected}')
