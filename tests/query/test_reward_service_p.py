"""Defines tests with SQL output fixture."""

from decimal import Decimal
from typing import Type

import pytest

from apps.math.models import CalculationTask, MathExercise
from apps.users.models import Balance, CustomUser
from services.reward_service.reward_service import RewardService


@pytest.fixture
def exercise_model() -> Type[CalculationTask]:
    """Fixture providing Calculation task model."""
    return CalculationTask


@pytest.fixture
def exercise_obj() -> CalculationTask:
    """Fixture providing Calculation task model."""
    return CalculationTask.objects.create(
        exercise=MathExercise.objects.create(name='adding')
    )


@pytest.mark.django_db
def test_add_reward_not_exist_balance(
    user: CustomUser,
    # Balans not exists
    exercise_model: Type[CalculationTask],
    exercise_obj: CalculationTask,
    debug_sql: None,
) -> None:
    """Test the reward service in the first time."""
    RewardService().add_reward(
        user=user,
        amount=Decimal(150),
        related_model=exercise_model,
        related_object=exercise_obj,
    )


@pytest.mark.django_db
def test_add_reward_exist_balance(
    user: CustomUser,
    balance: Balance,  # Balans exists
    exercise_model: Type[CalculationTask],
    exercise_obj: CalculationTask,
    debug_sql: None,
) -> None:
    """Test the reward service."""
    RewardService().add_reward(
        user=user,
        amount=Decimal(150),
        related_model=exercise_model,
        related_object=exercise_obj,
    )
