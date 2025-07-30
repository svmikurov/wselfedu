"""Tests for add reward Postgres procedure."""

from typing import Callable

import pytest
from django.db import connection

from apps.core.models import App
from apps.math.models.transaction import MathTransaction
from apps.users.models import Balance, CustomUser

AMOUNT = 33
SCHEMA_NAME = 'math'


@pytest.fixture
def user() -> CustomUser:
    """Fixture provides test user."""
    return CustomUser.objects.create_user(username='test_user')


@pytest.fixture(autouse=True)
def math_app() -> App:
    """Fixture provides math app."""
    return App.objects.create(name='Adding', schema_name=SCHEMA_NAME)


@pytest.fixture
def add_reward() -> Callable[..., None]:
    """Fixture to call reward procedure."""

    def _add_reward(
        user_id: int,
        amount: int = AMOUNT,
        schema: str = SCHEMA_NAME,
    ) -> None:
        with connection.cursor() as cursor:
            cursor.execute(
                'CALL increment_user_reward(%s, %s, %s)',
                (user_id, amount, schema),
            )

    return _add_reward


@pytest.mark.django_db
class TestIncrementUserRewardProcedure:
    """Test `increment_user_reward` Postgres procedure."""

    def test_transaction_created(
        self,
        user: CustomUser,
        add_reward: Callable[..., None],
    ) -> None:
        """Test transaction creation."""
        # Procedure call
        add_reward(user.pk)

        # Transaction created
        transaction = MathTransaction.objects.filter(user=user).first()

        # Added amount to transaction
        assert transaction is not None
        assert transaction.amount == AMOUNT

    def test_balance_updates(
        self,
        user: CustomUser,
        add_reward: Callable[..., None],
    ) -> None:
        """Test balance updates."""
        # Procedure call
        add_reward(user.pk)

        # Get user balance
        balance = Balance.objects.get(user=user)

        # Balance increased
        assert balance.total == AMOUNT

        # Call procedure
        add_reward(user.pk)

        # Balance Updated
        balance.refresh_from_db()
        assert balance.total == AMOUNT * 2
