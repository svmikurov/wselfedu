"""Contains tests of database table features."""

from datetime import timedelta

import pytest
from django.db import connection
from django.utils import timezone

from apps.math.models import MathExercise
from utils.sql.report.reporter import SQLReporter


@pytest.mark.django_db
def test_create_exercise_with_sql(
    debug_reporter: SQLReporter,
) -> None:
    """Test the auto-fill timestamp on create with row SQL.

    Test that the current datetime are set in the fild:
        - created_at
        - updated_at
    """
    # Act

    debug_reporter.start_act()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO math.exercise (name) VALUES (%s)',
            ('name',),
        )
    debug_reporter.end_act()

    # Assert

    # Get object
    obj = MathExercise.objects.get(name='name')

    # Object created
    assert MathExercise.objects.filter(name='name').exists()

    # The current datetime was set in the created_at field
    assert abs((obj.updated_at - timezone.now()).total_seconds()) < 1.0

    # The current datetime was set in the updated_at field
    assert abs((obj.created_at - timezone.now()).total_seconds()) < 1.0


@pytest.mark.django_db
def test_created_exercise_with_orm(
    debug_reporter: SQLReporter,
) -> None:
    """Test the auto-fill timestamp on create with ORM.

    Test that the current datetime are set in the fild:
        - created_at
        - updated_at
    """
    # Act
    debug_reporter.start_act()
    MathExercise.objects.create(name='name')
    debug_reporter.end_act()

    # Assert

    # Get object
    obj = MathExercise.objects.get(name='name')

    # Object created
    assert MathExercise.objects.filter(name='name').exists()
    # The current datetime was set in the created_at field
    assert abs((obj.created_at - timezone.now()).total_seconds()) < 1.0
    # The current datetime was set in the updated_at field
    assert abs((obj.updated_at - timezone.now()).total_seconds()) < 1.0


@pytest.mark.django_db
def test_updated_exercise_with_sql(
    debug_reporter: SQLReporter,
) -> None:
    """Test the auto-fill timestamp on update with row SQL.

    Test that the current datetime are set in the fild:
        - updated_at

    Test that the current datetime are NOT set in the fild:
        - created_at
    """
    # Setup

    before_time = timezone.now() - timedelta(days=1)
    obj = MathExercise.objects.create(
        name='name',
        created_at=before_time,
        updated_at=before_time,
    )

    # Act

    debug_reporter.start_act()
    connection.queries.clear()
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE math.exercise
            SET name = %s
            WHERE name = %s
            """,
            ('rename', 'name'),
        )
    debug_reporter.end_act()

    # Assert

    # Get object
    updated_obj = MathExercise.objects.get(name='rename')

    # Object updated
    assert not MathExercise.objects.filter(name='name').exists()
    assert MathExercise.objects.filter(name='rename').exists()
    assert updated_obj.id == obj.id

    # The current datetime was NOT set in the created_at field
    assert updated_obj.created_at == before_time

    # The current datetime was set in the updated_at field
    assert updated_obj.updated_at != before_time


@pytest.mark.django_db
def test_updated_exercise_with_orm(
    debug_reporter: SQLReporter,
) -> None:
    """Test the auto-fill timestamp on update with ORM request.

    Test that the current datetime are set in the fild:
        - updated_at

    Test that the current datetime are NOT set in the fild:
        - created_at
    """
    # Setup

    before_time = timezone.now() - timedelta(days=1)
    obj = MathExercise.objects.create(
        name='name',
        created_at=before_time,
        updated_at=before_time,
    )

    # Act

    debug_reporter.start_act()
    MathExercise.objects.filter(name='name').update(name='rename')
    debug_reporter.end_act()

    # Assert

    # Get object
    updated_obj = MathExercise.objects.get(name='rename')

    # Object updated
    assert not MathExercise.objects.filter(name='name').exists()
    assert MathExercise.objects.filter(name='rename').exists()
    assert updated_obj.id == obj.id

    # The current datetime was NOT set in the created_at field
    assert updated_obj.created_at == before_time

    # The current datetime was set in the updated_at field
    assert updated_obj.updated_at != before_time
