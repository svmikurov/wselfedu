"""Mathematical discipline calculation fixtures."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.contrib.contenttypes.models import ContentType

from apps.math.models import (
    CalculationCondition,
    CalculationTypeChoices,
    StudentCalculationCondition,
)
from apps.study.models import (
    ExerciseAvailability,
    ExerciseReward,
    PeriodExecuting,
    RewardType,
)
from apps.users.models import Mentorship

if TYPE_CHECKING:
    from apps.users.models import Person


@pytest.fixture
def calculation_condition(
    mentor: Person,
) -> CalculationCondition:
    """Populate DB with mentor`s calculation exercise conditions."""
    return CalculationCondition.objects.create(
        name='adding',
        min_operand=2,
        max_operand=3,
        operation_type=CalculationTypeChoices.ADD,
        user=mentor,
    )


@pytest.fixture
def calculation_assignation(
    calculation_condition: CalculationCondition,
    mentorship: Mentorship,
) -> StudentCalculationCondition:
    """Populate DB with assigned calculation exercise for student."""
    # Exercise assignation
    assignation = StudentCalculationCondition.objects.create(
        calculation_condition=calculation_condition,
        mentorship=mentorship,
    )
    # Exercise availability
    ExerciseAvailability.objects.create(
        exercise_content_type=ContentType.objects.get_for_model(assignation),
        exercise_object_id=assignation.pk,
        required_count=10,
        period_type=PeriodExecuting.DAILY,
    )
    # Exercise reward
    ExerciseReward.objects.create(
        exercise_content_type=ContentType.objects.get_for_model(assignation),
        exercise_object_id=assignation.pk,
        reward_type=RewardType.PER_CASE,
        amount=1,
    )
    return assignation
