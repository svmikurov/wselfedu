"""Calculation exercise repository."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypedDict, TypeVar, override

from django.contrib.contenttypes.models import ContentType
from django.db.models import F, OuterRef, Subquery
from django.utils import timezone

from apps.core.exceptions.storage import CacheMissError
from apps.core.handlers.protocol import DetailParamsProtocol
from apps.core.repositories.abstract import AbstractUserConditionsRepository
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
    PeriodExecuting,
)

if TYPE_CHECKING:
    from django.db.models import Manager

    from apps.core.storages.services.iabc import AbstractUserStorage
    from apps.math.models import CalculationCondition
    from apps.users.models import Person

__all__ = (
    'CalculationConditionsRepository',
    'StudentCalculationConditionsRepository',
)

ExerciseParameters = TypeVar('ExerciseParameters')


class CacheKeyDict(TypedDict):
    """Typed dict for cache key."""

    user_id: int
    prefix: str
    assignation_pk: int


class _BaseCalculationRepository(
    AbstractUserConditionsRepository[
        DetailParamsProtocol,
        ExerciseParameters,
    ],
    Generic[ExerciseParameters],
):
    """Base calculation repository."""

    STORAGE_PREFIX: str | None = None

    def __init__(
        self,
        storage: AbstractUserStorage[ExerciseParameters],
    ) -> None:
        """Construct the repository."""
        self._storage = storage

    @override
    def fetch(
        self, params: DetailParamsProtocol, user: Person
    ) -> ExerciseParameters:
        """Fetch calculation exercise conditions."""
        try:
            return self._storage.retrieve(**self._get_key(user, params))
        except CacheMissError:
            obj = self._get_object(params, user)
            self._storage.save(obj, **self._get_key(user, params))
            return obj

    def _get_object(
        self, params: DetailParamsProtocol, user: Person
    ) -> ExerciseParameters:
        raise NotImplementedError('Subclass must implement _get_object()')

    def _get_key(
        self, user: Person, params: DetailParamsProtocol
    ) -> CacheKeyDict:
        return {
            'user_id': user.pk,
            'prefix': self.storage_prefix,
            'assignation_pk': params.pk,
        }

    @property
    def storage_prefix(self) -> str:
        """Get storage prefix."""
        if not isinstance(self.STORAGE_PREFIX, str):
            raise AttributeError(
                f'{self.__class__.__name__} must define STORAGE_PREFIX '
                f'as `str`, got {type(self.STORAGE_PREFIX).__name__}'
            )
        return self.STORAGE_PREFIX


class CalculationConditionsRepository(
    _BaseCalculationRepository[RegularParametersDTO],
):
    """Calculation conditions repository."""

    STORAGE_PREFIX = 'calculation_conditions'

    def __init__(
        self,
        manager: Manager[CalculationCondition],
        storage: AbstractUserStorage[RegularParametersDTO],
    ) -> None:
        """Construct the repository."""
        self._manager = manager
        super().__init__(storage)

    @override
    def _get_object(
        self, params: DetailParamsProtocol, user: Person
    ) -> RegularParametersDTO:
        obj = self._manager.get(pk=params.pk, user=user)

        return RegularParametersDTO(
            conditions=CalculationConditionDTO(
                min_operand=obj.min_operand,
                max_operand=obj.max_operand,
                operation_type=obj.operation_type,  # type: ignore[arg-type]
            ),
        )


class StudentCalculationConditionsRepository(
    _BaseCalculationRepository[StudentParametersDTO,]
):
    """Student's assigned calculation conditions repository."""

    STORAGE_PREFIX = 'student_calculation_conditions'

    def __init__(
        self,
        manager: Manager[StudentCalculationCondition],
        storage: AbstractUserStorage[StudentParametersDTO],
    ) -> None:
        """Construct the repository."""
        self._manager = manager
        super().__init__(storage)

    @override
    def _get_object(
        self, params: DetailParamsProtocol, user: Person
    ) -> StudentParametersDTO:
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
                mentorship__student=user,
                calculation_condition_id=params.pk,
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
                success_count=self._get_success_count(obj),
                failure_count=obj.failure_count or 0,
                tracking_date=obj.tracking_date or timezone.now(),
            ),
            reward=ExerciseRewardDTO(
                reward_amount=obj.reward_amount,
                reward_type=obj.reward_type,
            ),
        )
        return parameters

    # REFACTOR: Implement reuse of method for other models.
    # TODO: Fix type ignore
    def _get_success_count(self, exercise: object) -> int:
        match exercise.period_type:  # type: ignore[attr-defined]
            case PeriodExecuting.APPOINTMENT:
                # REVIEW: Check implementation
                return exercise.success_count  # type: ignore
            case PeriodExecuting.DAILY:
                if exercise.tracking_date == timezone.now().date():  # type: ignore
                    return exercise.success_count  # type: ignore
                else:
                    return 0
            case _ as unexpected:
                raise ValueError(f'Unexpected period type {unexpected!r}')
