"""Mathematical discipline exercises."""

from datetime import datetime
from typing import Any, Protocol, override

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from apps.core.handlers.protocol import RequestContextProtocol
from apps.core.use_cases.abstract import AbstractUseCase
from apps.math.domains.dto import StudentExerciseDTO
from apps.math.models import StudentCalculationCondition
from apps.study.models import (
    ExerciseAvailability,
    ExerciseLog,
    ExerciseReward,
    PeriodExecuting,
)


class ExerciseQueryProtocol(Protocol):
    """Partial protocol for student's exercise query result."""

    period_type: PeriodExecuting
    required_count: int
    success_count: int
    is_completed: bool
    tracking_date: datetime


# HACK: Fix Any type hint
class StudentExercisesUseCase(
    AbstractUseCase[
        Any,
        RequestContextProtocol,
        Any,
        list[StudentExerciseDTO],
    ]
):
    """Student's exercises use case."""

    @override
    def execute(
        self,
        params: Any,
        context: RequestContextProtocol,
        validated: Any,
    ) -> list[StudentExerciseDTO]:
        """Get student's exercises assigned by mentor."""
        ct = ContentType.objects.get_for_model(StudentCalculationCondition)
        generic_relationship = {
            'exercise_content_type': ct,
            'exercise_object_id': models.OuterRef('pk'),
        }

        availability_subquery = ExerciseAvailability.objects.filter(
            **generic_relationship
        ).values('required_count')[:1]
        log_subquery = ExerciseLog.objects.filter(
            **generic_relationship
        ).values('success_count')[:1]
        reward_subquery = ExerciseReward.objects.filter(
            **generic_relationship
        ).values('reward_type')[:1]

        exercises_query = (
            StudentCalculationCondition.objects.filter(
                mentorship__student=context.user,
            )
            .select_related(
                'mentorship__student',
                'mentorship__mentor',
                'calculation_condition',
            )
            .annotate(
                # Exercise availability
                period_type=models.Subquery(
                    availability_subquery.values('period_type')[:1],
                    output_field=models.CharField(),
                ),
                required_count=models.Subquery(
                    availability_subquery.values('required_count')[:1],
                    output_field=models.IntegerField(),
                ),
                is_active=models.Subquery(
                    availability_subquery.values('is_active')[:1],
                    output_field=models.BooleanField(),
                ),
                is_completed=models.Subquery(
                    availability_subquery.values('is_completed')[:1],
                    output_field=models.BooleanField(),
                ),
                # Exercise log
                success_count=models.Subquery(
                    log_subquery.values('success_count')[:1],
                    output_field=models.IntegerField(),
                ),
                failure_count=models.Subquery(
                    log_subquery.values('failure_count')[:1],
                    output_field=models.IntegerField(),
                ),
                tracking_date=models.Subquery(
                    log_subquery.values('tracking_date')[:1],
                    output_field=models.DateField(),
                ),
                # Exercise reward
                reward_type=models.Subquery(
                    reward_subquery.values('reward_type')[:1],
                    output_field=models.CharField(),
                ),
                reward_amount=models.Subquery(
                    reward_subquery.values('amount')[:1],
                    output_field=models.DecimalField(),
                ),
            )
            .order_by('-created_at')
        )

        exercises: list[StudentExerciseDTO] = []

        for exercise in exercises_query:
            exercises.append(
                StudentExerciseDTO(
                    pk=exercise.pk,
                    name=exercise.calculation_condition.name,
                    mentor=exercise.mentorship.mentor.username,
                    # Availability
                    period_type=exercise.period_type,
                    required_count=exercise.required_count,
                    is_active=exercise.is_active,
                    is_completed=self._get_completion_state(exercise),
                    # Log
                    success_count=exercise.success_count,
                    failure_count=exercise.failure_count,
                    tracking_date=exercise.tracking_date,
                    # Reward
                    reward_type=exercise.reward_type,
                    reward_amount=exercise.reward_amount,
                )
            )

        return exercises

    def _get_completion_state(self, exercise: ExerciseQueryProtocol) -> bool:
        match exercise.period_type:
            case PeriodExecuting.APPOINTMENT:
                return exercise.is_completed
            case PeriodExecuting.DAILY:
                return (
                    exercise.required_count == exercise.success_count
                    and exercise.tracking_date == timezone.now().date()
                )
            case _ as unexpected:
                raise ValueError(f'Unexpected period type {unexpected!r}')
