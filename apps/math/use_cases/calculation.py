"""Calculation exercise use case."""

from __future__ import annotations

from typing import TYPE_CHECKING

from apps.core.storage.services.iabc import AbstractUserStorage
from apps.core.use_cases.abstract import AbstractUseCase
from apps.users.models.user import Person

from ..domains.dto import (
    CalculationAnswer,
    CalculationCase,
    CalculationConditions,
    CalculationExplain,
    CalculationMeta,
    CalculationResult,
)

if TYPE_CHECKING:
    from apps.core.service.exercise.abstract import (
        AbstractExerciseCheck,
        AbstractExerciseExplain,
        AbstractMilestone,
        AbstractRegularExerciseCreate,
    )

    type StorageService = AbstractUserStorage[CalculationMeta]
    type CreateService = AbstractRegularExerciseCreate[
        CalculationConditions,
        tuple[CalculationCase, CalculationMeta],
    ]
    type CheckService = AbstractExerciseCheck[
        CalculationAnswer, CalculationMeta, CalculationResult
    ]
    type MilestoneService = AbstractMilestone[
        CalculationResult, CalculationMeta
    ]
    type CreateUseCase = AbstractUseCase[
        CalculationConditions, CalculationCase
    ]
    type ExplainService = AbstractExerciseExplain[
        CalculationAnswer, CalculationMeta, CalculationExplain
    ]

CASE_STORE_PREFIX = 'regular_calculation_case'


class CalculationConditionsUseCase(
    AbstractUseCase[CalculationConditions, CalculationConditions],
):
    """Calculation conditions use case."""

    def execute(
        self,
        user: Person,
        request_data: CalculationConditions,
    ) -> CalculationConditions:
        """Start regular calculation exercise."""
        return request_data


class RegularCalculationCreateUseCase(
    AbstractUseCase[CalculationConditions, CalculationCase],
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
        request_data: CalculationConditions,
    ) -> CalculationCase:
        """Start regular calculation exercise."""
        case, meta = self._service.execute(request_data)
        self._storage.save(meta, user.pk, CASE_STORE_PREFIX)
        return case


class RegularCalculationCheckUseCase(
    AbstractUseCase[
        CalculationAnswer,
        CalculationCase | CalculationExplain,
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
        request_data: CalculationAnswer,
    ) -> CalculationCase | CalculationExplain:
        """Check regular calculation exercise."""
        meta = self._storage.retrieve(user.pk, CASE_STORE_PREFIX)
        result = self._check_service.execute(request_data, meta)

        if self._milestone_service:
            self._milestone_service.execute(user, result, meta)

        if result.is_correct:
            return self._create_use_case.execute(user, meta.conditions)
        else:
            return self._explain_service.execute(request_data, meta)
