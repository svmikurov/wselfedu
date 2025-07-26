"""Defines test of add reward Postgres procedure."""

import pytest
from django.db import connection

from apps.users.models import Balance
from utils.sql.report.reporter import SQLReporter

USER_ID = 1
AMOUNT = 33
# TODO: Add app table to DB
APP_NAME = 'math'

SQL_ADD_REWARD = 'CALL add_bonus(%s, %s, %s)', (USER_ID, AMOUNT, APP_NAME)


def add_math_reward() -> None:
    """Call procedure to add reward."""
    with connection.cursor() as cursor:
        cursor.execute(*SQL_ADD_REWARD)


@pytest.mark.django_db
def test_procedure_add_reward(debug_reporter: SQLReporter) -> None:
    """Test the add reward procedure."""
    # Act
    add_math_reward()

    # Assertion

    # Get data for assertions
    balance = Balance.objects.get(user_id=1)

    # The reward increased the balance
    assert balance.total == AMOUNT


@pytest.mark.django_db
def test_procedure_add_reward_twice(debug_reporter: SQLReporter) -> None:
    """Test the add reward procedure twice."""
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
