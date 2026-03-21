"""Detail exercise use case."""

from typing import TypeVar

from apps.core.assemblers.protocol import UserDetailCommandProtocol
from apps.core.domains.exercise.protocol import (
    CheckResultProtocol,
    Conditions,
    HasConditions,
)
from apps.core.factories.abstract import AbstractExerciseDTOFactory
from apps.core.services.exercise.abstract import (
    AbstractExerciseCheck,
    AbstractExerciseExplain,
    AbstractRegularExerciseCreate,
)
from apps.core.storages.services.iabc import AbstractUserStorage
from apps.core.use_cases.abstract import AbstractUseCase
from apps.math.domains.dto import (
    ExerciseAvailabilityDTO,
    ExerciseCompletionDTO,
    ExerciseRewardDTO,
)
from apps.math.milestones.protocol import MilestoneServiceProtocol
from apps.math.repositories.exercise import UserResourceRepository

CommandData = TypeVar('CommandData', bound=UserDetailCommandProtocol)

Case = TypeVar('Case')
CaseMeta = TypeVar('CaseMeta')
CheckResult = TypeVar('CheckResult', bound=CheckResultProtocol)

QueryResult = TypeVar('QueryResult')
ExerciseParameters = TypeVar('ExerciseParameters', bound=HasConditions)
ResultData = TypeVar('ResultData')


class ExerciseCreateUseCase(AbstractUseCase[CommandData, ResultData]):
    """Exercise start use case.

    Parameters
    ----------
    repository:
        Exercise perform parameters repository.
    service:
        Create exercise service.
    store_prefix:
        Store prefix for created exercise meta data.
    storage:
        Storage to store created exercise meta data.
    dto_factory:
        Use case result DTO factory.

    """

    def __init__(
        self,
        repository: UserResourceRepository[CommandData, ExerciseParameters],
        service: AbstractRegularExerciseCreate[
            Conditions,
            tuple[Case, CaseMeta],
        ],
        store_prefix: str,
        storage: AbstractUserStorage[CaseMeta],
        dto_factory: AbstractExerciseDTOFactory[
            Case,
            ExerciseParameters,
            ResultData,
        ],
    ) -> None:
        """Construct the use case."""
        self._store_prefix = store_prefix
        self._storage = storage
        self._repository = repository
        self._service = service
        self._dto_factory = dto_factory

    def execute(self, command: CommandData) -> ResultData:
        """Start stored exercise."""
        exercise_params = self._repository.fetch(command)
        case, meta = self._service.execute(exercise_params.conditions)
        self._storage.save(meta, command.user.pk, self._store_prefix)
        return self._dto_factory.create(case, exercise_params)


class ExerciseCheckUseCase(AbstractUseCase[CommandData, ResultData]):
    """Resource exercise check use case."""

    def __init__(
        self,
        store_prefix: str,
        storage: AbstractUserStorage[CaseMeta],
        check_service: AbstractExerciseCheck[
            CommandData,
            CaseMeta,
            CheckResult,
        ],
        repository: UserResourceRepository[CommandData, QueryResult],
        milestone_service: MilestoneServiceProtocol[
            CaseMeta,
            CheckResult,
            ExerciseAvailabilityDTO,
            ExerciseCompletionDTO,
            ExerciseRewardDTO,
        ]
        | None,
        create_use_case: AbstractUseCase[
            CommandData,
            ResultData,
        ],
        explain_service: AbstractExerciseExplain[
            CommandData,
            CaseMeta,
            ResultData,
        ],
    ) -> None:
        """Construct the use case."""
        self._store_prefix = store_prefix
        self._storage = storage
        self._check_service = check_service
        self._repository = repository
        self._milestone_service = milestone_service
        self._create_use_case = create_use_case
        self._explain_service = explain_service

    def execute(self, command: CommandData) -> ResultData:
        """Check student's exercise solution."""
        # Stored (cached) exercise case metadata contains
        # correct answer on current exercise case.
        meta = self._storage.retrieve(command.user.pk, self._store_prefix)
        result = self._check_service.execute(command.data, meta)

        # Stored (cached) exercise parameters contains
        # exercise availability and milestone data to update.
        exercise_parameters = self._repository.fetch(command)

        if self._milestone_service:
            self._milestone_service.execute(
                command.pk,
                command.user,
                meta,
                result,
                availability=exercise_parameters.availability,
                completion=exercise_parameters.completion,
                reward=exercise_parameters.reward,
            )

        if result.is_correct:
            return self._create_use_case.execute(command)
        else:
            return self._explain_service.execute(command, meta)
