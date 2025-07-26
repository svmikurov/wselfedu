"""Defines test of add reward Postgres procedure."""

import pytest
from django.db import connection
from django.db.models import Sum

from apps.math.models.transaction import MathTransaction
from apps.users.models import Balance, Transaction

USER_ID = 1
AMOUNT = 33
# TODO: Add app table to DB
APP_NAME = 'math'

SQL = 'CALL increment_user_reward(%s, %s, %s)', (USER_ID, AMOUNT, APP_NAME)


def add_math_reward() -> None:
    """Call procedure to add reward."""
    with connection.cursor() as cursor:
        cursor.execute(*SQL)


class TestIncrementUserRewardProcedure:
    """Test `increment_user_reward` Postgres procedure."""

    @pytest.mark.django_db
    def test_transaction_added(self) -> None:
        """Test that the transaction was added."""
        # Act
        add_math_reward()

        # Assertion

        # Get data for assertions
        transaction = Transaction.objects.filter(user_id=USER_ID)

        # Transaction was added once
        assert transaction.count() == 1

        # Transaction was added with amount
        assert transaction.last().amount == AMOUNT  # type: ignore[union-attr]

    @pytest.mark.django_db
    def test_math_transaction_added(self) -> None:
        """Test that the transaction was added to math transaction."""
        # Act
        add_math_reward()

        # Assertion

        # Get data for assertions
        transaction = MathTransaction.objects.filter(user_id=USER_ID)

        # Transaction was added once
        assert transaction.count() == 1

        # Transaction was added with amount
        assert transaction.last().amount == AMOUNT  # type: ignore[union-attr]

    @pytest.mark.django_db
    def test_transaction_added_twice(self) -> None:
        """Test that the transaction was added twice."""
        # Act
        add_math_reward()
        add_math_reward()

        # Assertion

        # Get data for assertions
        transaction = Transaction.objects.filter(user_id=USER_ID)
        total_amount = transaction.aggregate(total_amount=Sum('amount'))

        # Transaction was added once
        assert transaction.count() == 2

        # Transaction was added with amount
        assert total_amount.get('total_amount') == AMOUNT * 2

    @pytest.mark.django_db
    def test_balance_increased(self) -> None:
        """Test that balance increased."""
        # Act
        add_math_reward()

        # Assertion

        # Get data for assertions
        balance = Balance.objects.get(user_id=1)

        # The reward increased the balance
        assert balance.total == AMOUNT

    @pytest.mark.django_db
    def test_balance_increased_twice(self) -> None:
        """Test that balance increased, called twice."""
        # Setup
        double_reward = AMOUNT * 2

        # Act
        add_math_reward()
        add_math_reward()

        # Assertion

        # Get data for assertions
        balance = Balance.objects.get(user_id=1)

        # The reward increased the balance
        assert balance.total == double_reward
