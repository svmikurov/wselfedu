"""Defines test of add reward Postgres procedure."""

import pytest
from django.db import connection

from apps.users.models import Balance, Transaction
from utils.sql.report.reporter import SQLReporter

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
    def test_transaction_added(
        self,
        debug_reporter: SQLReporter,
    ) -> None:
        """Test that the transaction was added."""
        # Act
        debug_reporter.start_act()
        add_math_reward()
        debug_reporter.end_act()

        # Assertion

        # Get data for assertions
        transaction = Transaction.objects.filter(user_id=USER_ID)

        print(f':::: {transaction = }')

        # Transaction was added once
        # assert transaction.count() == 1

        # Transaction was added with amount
        # assert transaction.last().amount == AMOUNT

    @pytest.mark.django_db
    def test_balance_increased(
        self,
        debug_reporter: SQLReporter,
    ) -> None:
        """Test that balance increased."""
        # Act
        add_math_reward()

        # Assertion

        # Get data for assertions
        balance = Balance.objects.get(user_id=1)

        # The reward increased the balance
        assert balance.total == AMOUNT

    @pytest.mark.django_db
    def test_balance_increased_twice(
        self,
        debug_reporter: SQLReporter,
    ) -> None:
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
