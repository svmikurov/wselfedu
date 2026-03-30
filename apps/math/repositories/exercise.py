"""Calculation exercise repository."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from django.contrib.contenttypes.models import ContentType
from django.db.models import F, OuterRef, Subquery
from django.utils import timezone

from apps.core.assemblers.command import UserDetailCommand
from apps.core.repositories.generic import UserResourceCachedRepository
from apps.math.domains.dto import (
    CalculationConditionDTO,
    ExerciseAvailabilityDTO,
    ExerciseCompletionDTO,
    ExerciseRewardDTO,
    RegularParametersDTO,
    StudentParametersDTO,
)
from apps.math.models import StudentCalculationCondition
from apps.study.models import (
    ExerciseAvailability,
    ExerciseLog,
    ExerciseReward,
)
from apps.study.resolvers.protocol import CompletionResolverProtocol

if TYPE_CHECKING:
    from django.db.models import Manager

    from apps.core.storages.services.iabc import AbstractUserStorage
    from apps.math.models import CalculationCondition

__all__ = (
    'CalculationConditionsRepository',
    'StudentCalculationConditionsRepository',
)


class CalculationConditionsRepository(
    UserResourceCachedRepository[UserDetailCommand, RegularParametersDTO],
):
    """Calculation conditions repository."""

    def __init__(
        self,
        store_prefix: str,
        storage: AbstractUserStorage[RegularParametersDTO],
        manager: Manager[CalculationCondition],
    ) -> None:
        """Construct the repository."""
        self._manager = manager
        super().__init__(store_prefix, storage)

    @override
    def _get_object(self, command: UserDetailCommand) -> RegularParametersDTO:
        obj = self._manager.get(pk=command.pk, user=command.user)

        return RegularParametersDTO(
            conditions=CalculationConditionDTO(
                min_operand=obj.min_operand,
                max_operand=obj.max_operand,
                operation_type=obj.operation_type,  # type: ignore[arg-type]
            ),
        )


class StudentCalculationConditionsRepository(
    UserResourceCachedRepository[UserDetailCommand, StudentParametersDTO],
):
    """Student's assigned calculation conditions repository."""

    def __init__(
        self,
        store_prefix: str,
        storage: AbstractUserStorage[StudentParametersDTO],
        manager: Manager[StudentCalculationCondition],
        resolver: CompletionResolverProtocol,
    ) -> None:
        """Construct the repository."""
        self._manager = manager
        self._resolver = resolver
        super().__init__(store_prefix, storage)

    @override
    def _get_object(self, command: UserDetailCommand) -> StudentParametersDTO:
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

        completion_log = ExerciseLog.objects.filter(
            exercise_content_type=exercise_content_type,
            exercise_object_id=OuterRef('pk'),
        ).values(
            'success_count',
            'failure_count',
            'tracking_date',
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
                # Completion log
                success_count=Subquery(completion_log.values('success_count')),
                failure_count=Subquery(completion_log.values('failure_count')),
                tracking_date=Subquery(completion_log.values('tracking_date')),
            )
            .get(
                mentorship__student=command.user,
                calculation_condition_id=command.pk,
            )
        )

        parameters = StudentParametersDTO(
            conditions=CalculationConditionDTO(
                min_operand=obj.min_operand,
                max_operand=obj.max_operand,
                operation_type=obj.operation_type,
            ),
            availability=ExerciseAvailabilityDTO(
                required_count=obj.required_count,
                period_type=obj.period_type,
                started_at=obj.started_at,
                is_active=obj.is_active,
                is_completed=obj.is_completed,
                completed_at=obj.completed_at,
            ),
            completion=ExerciseCompletionDTO(
                success_count=self._resolver.get_success_count(obj),  # type: ignore[arg-type]
                failure_count=obj.failure_count or 0,
                tracking_date=obj.tracking_date or timezone.now(),
            ),
            reward=ExerciseRewardDTO(
                reward_amount=obj.reward_amount,
                reward_type=obj.reward_type,
            ),
        )
        return parameters
