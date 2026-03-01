"""Calculation exercise repository."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from django.contrib.contenttypes.models import ContentType
from django.db.models import F, OuterRef, Subquery

from apps.core.exceptions.storage import CacheMissError
from apps.core.handlers.protocol import DetailParamsProtocol
from apps.core.repositories.abstract import AbstractUserConditionsRepository
from apps.math.domains.dto import (
    CalculationConditionDTO,
    ExerciseAvailabilityDTO,
    ExerciseMilestoneDTO,
    ExerciseParametersDTO,
)
from apps.math.models import StudentCalculationCondition
from apps.study.models import ExerciseAvailability, ExerciseReward

if TYPE_CHECKING:
    from django.db.models import Manager

    from apps.core.storages.services.iabc import AbstractUserStorage
    from apps.math.models import CalculationCondition
    from apps.users.models import Person

__all__ = (
    'CalculationConditionsRepository',
    'StudentCalculationConditionsRepository',
)


class _BaseCalculationRepository(
    AbstractUserConditionsRepository[
        DetailParamsProtocol,
        ExerciseParametersDTO,
    ],
):
    """Base calculation repository."""

    STORAGE_PREFIX: str | None = None

    def __init__(
        self,
        storage: AbstractUserStorage[ExerciseParametersDTO],
    ) -> None:
        """Construct the repository."""
        self._storage = storage

    @override
    def fetch(
        self, params: DetailParamsProtocol, user: Person
    ) -> ExerciseParametersDTO:
        """Fetch calculation exercise conditions."""
        try:
            return self._storage.retrieve(user.pk, self.storage_prefix)
        except CacheMissError:
            obj = self._get_object(params, user)
            self._storage.save(obj, user.pk, self.storage_prefix)
            return obj

    def _get_object(
        self, params: DetailParamsProtocol, user: Person
    ) -> ExerciseParametersDTO:
        raise NotImplementedError('Subclass must implement _get_object()')

    @property
    def storage_prefix(self) -> str:
        """Get storage prefix."""
        if not isinstance(self.STORAGE_PREFIX, str):
            raise AttributeError(
                f'{self.__class__.__name__} must define STORAGE_PREFIX '
                f'as `str`, got {type(self.STORAGE_PREFIX).__name__}'
            )
        return self.STORAGE_PREFIX


class CalculationConditionsRepository(_BaseCalculationRepository):
    """Calculation conditions repository."""

    STORAGE_PREFIX = 'calculation_conditions'

    def __init__(
        self,
        manager: Manager[CalculationCondition],
        storage: AbstractUserStorage[ExerciseParametersDTO],
    ) -> None:
        """Construct the repository."""
        self._manager = manager
        super().__init__(storage)

    @override
    def _get_object(
        self, params: DetailParamsProtocol, user: Person
    ) -> ExerciseParametersDTO:
        obj = self._manager.get(pk=params.pk, user=user)

        return ExerciseParametersDTO(
            conditions=CalculationConditionDTO(
                min_operand=obj.min_operand,
                max_operand=obj.max_operand,
                operation_type=obj.operation_type,  # type: ignore[arg-type]
            ),
        )


class StudentCalculationConditionsRepository(_BaseCalculationRepository):
    """Student's assigned calculation conditions repository."""

    STORAGE_PREFIX = 'student_calculation_conditions'

    def __init__(
        self,
        manager: Manager[StudentCalculationCondition],
        storage: AbstractUserStorage[ExerciseParametersDTO],
    ) -> None:
        """Construct the repository."""
        self._manager = manager
        super().__init__(storage)

    @override
    def _get_object(
        self, params: DetailParamsProtocol, user: Person
    ) -> ExerciseParametersDTO:
        exercise_content_type = ContentType.objects.get_for_model(
            StudentCalculationCondition
        )

        reward = ExerciseReward.objects.filter(
            exercise_content_type=exercise_content_type,
            exercise_object_id=OuterRef('pk'),
        ).values(
            'amount',
            'reward_type',
        )[:1]

        availability = ExerciseAvailability.objects.filter(
            exercise_content_type=exercise_content_type,
            exercise_object_id=OuterRef('pk'),
        ).values(
            'required_count',
            'period_type',
            'started_at',
            'is_active',
            'is_completed',
            'completed_at',
        )[:1]

        obj = (
            self._manager.select_related(
                'calculation_condition',
            )
            .annotate(
                # Calculation conditions
                min_operand=F('calculation_condition__min_operand'),
                max_operand=F('calculation_condition__max_operand'),
                operation_type=F('calculation_condition__operation_type'),
                # Reward
                reward_amount=Subquery(reward.values('amount')),
                reward_type=Subquery(reward.values('reward_type')),
                # Availability
                required_count=Subquery(availability.values('required_count')),
                period_type=Subquery(availability.values('period_type')),
                started_at=Subquery(availability.values('started_at')),
                is_active=Subquery(availability.values('is_active')),
                is_completed=Subquery(availability.values('is_completed')),
                completed_at=Subquery(availability.values('completed_at')),
            )
            .get(
                mentorship__student=user,
                calculation_condition_id=params.pk,
            )
        )

        return ExerciseParametersDTO(
            conditions=CalculationConditionDTO(
                min_operand=obj.min_operand,
                max_operand=obj.max_operand,
                operation_type=obj.operation_type,
            ),
            milestone=ExerciseMilestoneDTO(
                reward_amount=obj.reward_amount,
                reward_type=obj.reward_type,
            ),
            availability=ExerciseAvailabilityDTO(
                required_count=obj.required_count,
                period_type=obj.period_type,
                started_at=obj.started_at,
                is_active=obj.is_active,
                is_completed=obj.is_completed,
                completed_at=obj.completed_at,
            ),
        )
