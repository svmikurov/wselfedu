"""Contains tests of database table features."""

import pytest
from django.db import connection

from apps.math.models import MathExercise
from utils.sql.sql_reporter import SQLReporter


@pytest.mark.django_db
def test_updated_at(
    debug_reporter: SQLReporter,
) -> None:
    """Test the auto-fill of the add row field."""
    debug_reporter.start_act()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO math_exercise (name) VALUES (%s)',
            ('new',),
            # 'VALUES (%s, %s, %s)',
            # ('new', timezone.now(), timezone.now()),
        )
    debug_reporter.end_act()

    obj = MathExercise.objects.get(name='new')
    print(f':::::::: {obj.created_at = }')
    print(f':::::::: {obj.updated_at = }')
