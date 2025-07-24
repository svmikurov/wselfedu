"""Contains tests of database table features."""

import pytest
from django.db import connection
from django.utils import timezone

from apps.math.models import MathExercise
from utils.sql.sql_reporter import SQLReporter


@pytest.mark.django_db
def test_updated_at(
    debug_reporter: SQLReporter,
) -> None:
    """Test the auto-fill of the add row field."""
    # Setup
    before_time = timezone.now()

    # Act
    debug_reporter.start_act()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO math_exercise (name) VALUES (%s)',
            ('new',),
        )
    debug_reporter.end_act()

    # Assert
    obj = MathExercise.objects.get(name='new')
    assert abs((obj.updated_at - before_time).total_seconds()) < 1.0
    assert abs((obj.created_at - before_time).total_seconds()) < 1.0
