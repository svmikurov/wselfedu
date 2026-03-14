"""Detail exercise use case."""

from typing import TypeVar

from apps.core.domains.exercise.types import CheckResultProtocol
from apps.core.domains.null import NullDTO
from apps.core.factories.abstract import AbstractExerciseDTOFactory
from apps.core.handlers.protocol import (
    DetailRequestParamsProtocol,
    RequestContextProtocol,
)
from apps.core.services.exercise.abstract import (
    AbstractExerciseCheck,
    AbstractExerciseExplain,
    AbstractRegularExerciseCreate,
)
from apps.core.storages.services.iabc import AbstractUserStorage
from apps.core.use_cases.abstract import AbstractUseCase
from apps.math.domains.dto import (
    CalculationCaseDTO,
    CalculationConditionDTO,
    CalculationMetaDTO,
    ExerciseAvailabilityDTO,
    ExerciseCompletionDTO,
    ExerciseRewardDTO,
    RegularParametersDTO,
    StudentCalculationDTO,
)
from apps.math.milestones.protocol import MilestoneServiceProtocol
from apps.math.repositories.exercise import BaseExerciseRepository

ResultDTO = TypeVar('ResultDTO')
ExerciseParamsDTO = TypeVar('ExerciseParamsDTO', bound=RegularParametersDTO)
UserAnswer = TypeVar('UserAnswer')
CheckResult = TypeVar('CheckResult', bound=CheckResultProtocol)
CaseMeta = TypeVar('CaseMeta')
ResultData = TypeVar('ResultData')


class DetailExerciseCreateUseCase(
    AbstractUseCase[
        DetailRequestParamsProtocol,
        RequestContextProtocol,
        NullDTO,
        CalculationCaseDTO,
    ],
):
    """Start stored exercise use case."""

    def __init__(
        self,
        store_prefix: str,
        storage: AbstractUserStorage[CalculationMetaDTO],
        repository: BaseExerciseRepository[ExerciseParamsDTO],
        service: AbstractRegularExerciseCreate[
            CalculationConditionDTO,
            tuple[CalculationCaseDTO, CalculationMetaDTO],
        ],
        dto_factory: AbstractExerciseDTOFactory[
            CalculationCaseDTO,
            RegularParametersDTO,
            CalculationCaseDTO,
        ],
    ) -> None:
        """Construct the use case."""
        self._store_prefix = store_prefix
        self._storage = storage
        self._repository = repository
        self._service = service
        self._dto_factory = dto_factory

    def execute(
        self,
        params: DetailRequestParamsProtocol,
        context: RequestContextProtocol,
        validated: NullDTO,
    ) -> CalculationCaseDTO:
        """Start stored exercise."""
        exercise_params = self._repository.fetch(params, context.user)
        case, meta = self._service.execute(exercise_params.conditions)
        self._storage.save(meta, context.user.pk, self._store_prefix)
        return self._dto_factory.create(case, exercise_params)


class DetailCalculationCheckUseCase(
    AbstractUseCase[
        DetailRequestParamsProtocol,
        RequestContextProtocol,
        UserAnswer,
        ResultData,
    ],
):
    """Detail calculation check use case."""

    def __init__(
        self,
        store_prefix: str,
        storage: AbstractUserStorage[CaseMeta],
        check_service: AbstractExerciseCheck[
            UserAnswer,
            CaseMeta,
            CheckResult,
        ],
        repository: BaseExerciseRepository[StudentCalculationDTO],
        milestone_service: MilestoneServiceProtocol[
            CaseMeta,
            CheckResult,
            ExerciseAvailabilityDTO,
            ExerciseCompletionDTO,
            ExerciseRewardDTO,
        ]
        | None,
        create_use_case: AbstractUseCase[
            DetailRequestParamsProtocol,
            RequestContextProtocol,
            NullDTO,
            ResultData,
        ],
        explain_service: AbstractExerciseExplain[
            UserAnswer,
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

    def execute(
        self,
        params: DetailRequestParamsProtocol,
        context: RequestContextProtocol,
        validated: UserAnswer,
    ) -> ResultData:
        """Check student's exercise solution."""
        # Stored (cached) exercise case metadata contains
        # correct answer on current exercise case.
        meta = self._storage.retrieve(context.user.pk, self._store_prefix)
        result = self._check_service.execute(validated, meta)

        # Stored (cached) exercise parameters contains
        # exercise availability and milestone data to update.
        exercise_parameters = self._repository.fetch(params, context.user)

        if self._milestone_service:
            self._milestone_service.execute(
                params.pk,
                context.user,
                meta,
                result,
                availability=exercise_parameters.availability,
                completion=exercise_parameters.completion,
                reward=exercise_parameters.reward,
            )

        if result.is_correct:
            return self._create_use_case.execute(params, context, NullDTO())
        else:
            return self._explain_service.execute(validated, meta)
