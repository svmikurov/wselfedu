"""Defines tests of reward service."""

from decimal import Decimal
from typing import Type

import pytest

from apps.math.models import MathExercise
from apps.math.models.calculation import CalculationTask
from apps.users.models import Balance, CustomUser
from services.reward_service.reward import RewardService
from utils.sql.report.reporter import SQLReporter


@pytest.fixture
def exercise_model() -> Type[CalculationTask]:
    """Fixture providing Calculation task model."""
    return CalculationTask


@pytest.fixture
def calc_task() -> CalculationTask:
    """Fixture providing calculation task."""
    return CalculationTask.objects.create(  # type: ignore[attr-defined, no-any-return]
        exercise=MathExercise.objects.create(name='adding'),
        operand_1=3,
        operand_2=4,
    )


@pytest.mark.skip('Add "math_calculation_task" table to DB')
@pytest.mark.django_db
def test_add_reward_not_exist_balance(
    user: CustomUser,
    # Balans not exists
    exercise_model: Type[CalculationTask],
    calc_task: CalculationTask,
    debug_reporter: SQLReporter,
) -> None:
    """Test of the first reward with balance creation."""
    # Setup
    reward = Decimal(333)
    assert not Balance.objects.filter(user=user).exists()

    # Act

    debug_reporter.start_act()

    RewardService().add_reward(
        user=user,
        amount=reward,
        related_model=exercise_model,
        related_object=calc_task,
    )

    debug_reporter.end_act()

    # Assert

    # Balance created
    assert Balance.objects.filter(user=user).exists()

    # Get balance
    balance = Balance.objects.only('amount').get(user=user)

    # Added reward to balance
    assert balance.amount == reward

    # Get all transactions for this balance
    transactions = balance.transactions.all()

    # Transaction create one record
    assert transactions.count() == 1


@pytest.mark.skip
@pytest.mark.django_db
def test_add_reward_exist_balance(
    user: CustomUser,
    balance: Balance,  # Balans exists
    exercise_model: Type[CalculationTask],
    calc_task: CalculationTask,
    debug_reporter: SQLReporter,
) -> None:
    """Test reward with existing balance."""
    # Setup
    reward = Decimal(333)
    assert Balance.objects.filter(user=user).exists()

    # Act
    debug_reporter.start_act()

    RewardService().add_reward(
        user=user,
        amount=reward,
        related_model=exercise_model,
        related_object=calc_task,
    )

    debug_reporter.end_act()

    # Assert

    balances = Balance.objects.filter(user=user)

    # Balance not added
    assert balances.count() == 1

    # Get the balance
    balance = Balance.objects.get(user=user)

    # Added reward to balance
    assert balance.amount == reward

    # Get all transactions for this balance
    transactions = balance.transactions.all()

    # Transaction create one record
    assert transactions.count() == 1
