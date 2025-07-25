"""Defines test of add reward Postgres procedure."""

import pytest
from django.db import connection

from utils.sql.report.reporter import SQLReporter

sql = 'CALL add_bonus(%s, %s, %s)', (1, 33, 'math')


@pytest.mark.django_db
def test_procedure_add_reward(debug_reporter: SQLReporter) -> None:
    """Test the add reward procedure."""
    with connection.cursor() as cursor:
        cursor.execute(*sql)
