"""Calculation exercise use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from apps.core.handlers.protocol import (
    DetailParamsProtocol,
    RequestContextProtocol,
)
from apps.core.storage.services.iabc import AbstractUserStorage
from apps.core.use_cases.abstract import AbstractDetailUseCase, AbstractUseCase
from apps.users.models.user import Person

from ..domains.dto import (
    CalculationAnswerDTO,
    CalculationCaseDTO,
    CalculationConditionDTO,
    CalculationExplainDTO,
    CalculationMetaDTO,
    CalculationResultDTO,
)

if TYPE_CHECKING:
    from apps.core.service.exercise.abstract import (
        AbstractExerciseCheck,
        AbstractExerciseExplain,
        AbstractMilestone,
        AbstractRegularExerciseCreate,
    )

    # HACK: Fix Any type hint
    type ParametersRepository = Any

    type StorageService = AbstractUserStorage[CalculationMetaDTO,]
    type CreateService = AbstractRegularExerciseCreate[
        CalculationConditionDTO,
        tuple[CalculationCaseDTO, CalculationMetaDTO],
    ]
    type CheckService = AbstractExerciseCheck[
        CalculationAnswerDTO, CalculationMetaDTO, CalculationResultDTO
    ]
    type MilestoneService = AbstractMilestone[
        CalculationResultDTO, CalculationMetaDTO
    ]
    type CreateUseCase = AbstractUseCase[
        CalculationConditionDTO, CalculationCaseDTO
    ]
    type CreateDetailUseCase = AbstractDetailUseCase[CalculationCaseDTO,]
    type ExplainService = AbstractExerciseExplain[
        CalculationAnswerDTO, CalculationMetaDTO, CalculationExplainDTO
    ]

type RequestData = dict[str, Any]

CASE_STORE_PREFIX = 'regular_calculation_case'


class CalculationConditionsUseCase(
    AbstractUseCase[CalculationConditionDTO, CalculationConditionDTO],
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
    AbstractUseCase[CalculationConditionDTO, CalculationCaseDTO],
):
    """Start regular calculation use case."""

    def __init__(
        self,
        service: CreateService,
        storage: StorageService,
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
    AbstractUseCase[
        CalculationAnswerDTO,
        CalculationCaseDTO | CalculationExplainDTO,
    ],
):
    """Regular calculation check use case."""

    def __init__(
        self,
        storage: StorageService,
        check_service: CheckService,
        milestone_service: MilestoneService,
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
        request_data: CalculationAnswerDTO,
    ) -> CalculationCaseDTO | CalculationExplainDTO:
        """Check regular calculation exercise."""
        meta = self._storage.retrieve(user.pk, CASE_STORE_PREFIX)
        result = self._check_service.execute(request_data, meta)

        if self._milestone_service:
            self._milestone_service.execute(user, result, meta)

        if result.is_correct:
            return self._create_use_case.execute(user, meta.conditions)
        else:
            return self._explain_service.execute(request_data, meta)


class DetailCalculationCreateUseCase:
    """Start stored calculation exercise use case."""

    def __init__(
        self,
        repository: ParametersRepository,
        service: CreateService,
        storage: StorageService,
    ) -> None:
        """Construct the use case."""
        self._repository = repository
        self._service = service
        self._storage = storage

    def execute(
        self,
        params: DetailParamsProtocol,
        context: RequestContextProtocol,
        # HACK: Unify the use case interface
        # for data parameter in requests without a body.
        data: object,
    ) -> CalculationCaseDTO:
        """Start stored calculation exercise."""
        conditions = self._repository.fetch(params, context.user.pk)
        case, meta = self._service.execute(conditions)
        self._storage.save(meta, context.user.pk, CASE_STORE_PREFIX)
        return case


class DetailCalculationCheckUseCase:
    """Detail calculation check use case."""

    def __init__(
        self,
        storage: StorageService,
        check_service: CheckService,
        milestone_service: MilestoneService,
        create_use_case: CreateDetailUseCase,
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
        params: DetailParamsProtocol,
        context: RequestContextProtocol,
        data: CalculationAnswerDTO,
    ) -> CalculationCaseDTO | CalculationExplainDTO:
        """Check regular calculation exercise."""
        meta = self._storage.retrieve(context.user.pk, CASE_STORE_PREFIX)
        result = self._check_service.execute(data, meta)

        if self._milestone_service:
            self._milestone_service.execute(context.user, result, meta)

        if result.is_correct:
            return self._create_use_case.execute(params, context, data)
        else:
            return self._explain_service.execute(data, meta)
