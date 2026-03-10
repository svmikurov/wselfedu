"""Calculation exercise use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from apps.core.factories.abstract import AbstractExerciseDTOFactory
from apps.core.handlers.protocol import (
    DetailParamsProtocol,
    RequestContextProtocol,
)
from apps.core.storages.services.iabc import AbstractUserStorage
from apps.core.use_cases.abstract import (
    AbstractDataUseCase,
    AbstractDetailDataUseCase,
    AbstractDetailUseCase,
)
from apps.math.repositories.exercise import (
    StudentCalculationConditionsRepository,
)
from apps.users.models.user import Person

from ..domains.dto import (
    CalculationAnswerDTO,
    CalculationCaseDTO,
    CalculationConditionDTO,
    CalculationDomainDTO,
    CalculationDTO,
    CalculationExplainDTO,
    CalculationLoopDTO,
    CalculationMetaDTO,
    CalculationResultDTO,
    ExerciseAvailabilityDTO,
    ExerciseCompletionDTO,
    ExerciseRewardDTO,
    StudentParametersDTO,
)

if TYPE_CHECKING:
    from apps.core.services.exercise.abstract import (
        AbstractExerciseCheck,
        AbstractExerciseExplain,
        AbstractMilestone,
        AbstractRegularExerciseCreate,
    )
    from apps.math.milestones.protocol import MilestoneServiceProtocol

    type ParametersRepository = StudentCalculationConditionsRepository
    type CreateService = AbstractRegularExerciseCreate[
        CalculationConditionDTO,
        tuple[CalculationCaseDTO, CalculationMetaDTO],
    ]
    type StudentCreateService = AbstractRegularExerciseCreate[
        CalculationConditionDTO,
        tuple[CalculationDomainDTO, CalculationMetaDTO],
    ]
    type StudentDTOFactory = AbstractExerciseDTOFactory[
        CalculationCaseDTO,
        StudentParametersDTO,
        CalculationDTO,
    ]
    type CheckService = AbstractExerciseCheck[
        CalculationAnswerDTO,
        CalculationCaseDTO,
        CalculationResultDTO,
    ]
    type MilestoneService = AbstractMilestone[
        CalculationResultDTO,
        CalculationCaseDTO,
    ]
    type DetailMilestoneService = MilestoneServiceProtocol[
        CalculationMetaDTO,
        CalculationResultDTO,
        ExerciseAvailabilityDTO,
        ExerciseCompletionDTO,
        ExerciseRewardDTO,
    ]
    type CreateUseCase = AbstractDataUseCase[
        CalculationConditionDTO,
        CalculationCaseDTO,
    ]
    type CreateDetailUseCase = AbstractDetailUseCase[CalculationCaseDTO]
    type ExplainService = AbstractExerciseExplain[
        CalculationAnswerDTO,
        CalculationCaseDTO,
        CalculationExplainDTO,
    ]

type RequestData = dict[str, Any]

CASE_STORE_PREFIX = 'regular_calculation_case'


class CalculationConditionsUseCase(
    AbstractDataUseCase[CalculationConditionDTO, CalculationConditionDTO],
):
    """Calculation conditions use case."""

    def execute(
        self,
        user: Person,
        request_data: CalculationConditionDTO,
    ) -> CalculationConditionDTO:
        """Start regular calculation exercise."""
        return request_data


class RegularCalculationCreateUseCase(
    AbstractDataUseCase[CalculationConditionDTO, CalculationCaseDTO],
):
    """Start regular calculation use case."""

    def __init__(
        self,
        service: CreateService,
        storage: AbstractUserStorage[CalculationMetaDTO],
    ) -> None:
        """Construct the use case."""
        self._service = service
        self._storage = storage

    def execute(
        self,
        user: Person,
        request_data: CalculationConditionDTO,
    ) -> CalculationCaseDTO:
        """Start regular calculation exercise."""
        case, meta = self._service.execute(request_data)
        self._storage.save(meta, user.pk, CASE_STORE_PREFIX)
        return case


class RegularCalculationCheckUseCase(
    AbstractDataUseCase[
        CalculationLoopDTO,
        CalculationCaseDTO | CalculationExplainDTO,
    ],
):
    """Regular calculation check use case."""

    def __init__(
        self,
        storage: AbstractUserStorage[CalculationMetaDTO],
        check_service: CheckService,
        milestone_service: MilestoneService | None,
        create_use_case: CreateUseCase,
        explain_service: ExplainService,
    ) -> None:
        """Construct the use case."""
        self._storage = storage
        self._check_service = check_service
        self._milestone_service = milestone_service
        self._create_use_case = create_use_case
        self._explain_service = explain_service

    def execute(
        self,
        user: Person,
        request_data: CalculationLoopDTO,
    ) -> CalculationCaseDTO | CalculationExplainDTO:
        """Check regular calculation exercise."""
        meta = self._storage.retrieve(user.pk, CASE_STORE_PREFIX)
        result = self._check_service.execute(request_data, meta)

        if self._milestone_service:
            self._milestone_service.execute(user, result, meta)

        if result.is_correct:
            return self._create_use_case.execute(user, request_data)
        else:
            return self._explain_service.execute(request_data, meta)


# =================================================
# Detail calculation create/check exercise services
# =================================================


# REFACTOR: Relocate to core app as core use case to create exercise
class DetailExerciseCreateUseCase(AbstractDetailUseCase[CalculationDTO]):
    """Start stored exercise use case."""

    def __init__(
        self,
        repository: ParametersRepository,
        service: CreateService,
        storage: AbstractUserStorage[CalculationMetaDTO],
        dto_factory: StudentDTOFactory,
    ) -> None:
        """Construct the use case."""
        self._repository = repository
        self._service = service
        self._storage = storage
        self._dto_factory = dto_factory

    def execute(
        self,
        params: DetailParamsProtocol,
        context: RequestContextProtocol,
        # HACK: Unify the use case interface
        # for data parameter in requests without a body.
        data: object,
    ) -> CalculationDTO:
        """Start stored exercise."""
        parameters = self._repository.fetch(params, context.user)
        case, meta = self._service.execute(parameters.conditions)
        self._storage.save(meta, context.user.pk, CASE_STORE_PREFIX)
        return self._dto_factory.create(case, parameters)


class DetailCalculationCheckUseCase(
    AbstractDetailDataUseCase[
        CalculationAnswerDTO,
        CalculationCaseDTO | CalculationExplainDTO,
    ]
):
    """Detail calculation check use case."""

    def __init__(
        self,
        storage: AbstractUserStorage[CalculationMetaDTO],
        check_service: CheckService,
        repository: ParametersRepository,
        milestone_service: DetailMilestoneService,
        create_use_case: CreateDetailUseCase,
        explain_service: ExplainService,
    ) -> None:
        """Construct the use case."""
        self._storage = storage
        self._check_service = check_service
        self._repository = repository
        self._milestone_service = milestone_service
        self._create_use_case = create_use_case
        self._explain_service = explain_service

    def execute(
        self,
        params: DetailParamsProtocol,
        context: RequestContextProtocol,
        data: CalculationAnswerDTO,
    ) -> CalculationCaseDTO | CalculationExplainDTO:
        """Check student's exercise solution."""
        # Stored (cached) exercise case metadata contains
        # correct answer on current exercise case.
        meta = self._storage.retrieve(context.user.pk, CASE_STORE_PREFIX)
        result = self._check_service.execute(data, meta)

        # Stored (cached) exercise parameters contains
        # exercise availability and milestone data to update.
        exercise_parameters = self._repository.fetch(params, context.user)
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
            # HACK: Fix None pass to use case
            return self._create_use_case.execute(params, context, None)
        else:
            return self._explain_service.execute(data, meta)
