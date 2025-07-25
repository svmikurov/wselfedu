"""Contains tests of database table features."""

from datetime import timedelta

import pytest
from django.db import IntegrityError, connection, transaction
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
            'INSERT INTO math_exercise (name) VALUES (%s)',
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


@pytest.mark.skip('Fix: Trigger for datetime update is not applied in test DB')
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
            UPDATE math_exercise
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
    assert obj.id == updated_obj.id

    # The current datetime was NOT set in the created_at field
    assert obj.created_at == before_time

    # The current datetime was set in the updated_at field
    assert obj.updated_at != before_time


@pytest.mark.skip('Fix: Trigger for datetime update is not applied in test DB')
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
    assert obj.id == updated_obj.id

    # The current datetime was NOT set in the created_at field
    assert obj.created_at == before_time

    # The current datetime was set in the updated_at field
    assert obj.updated_at != before_time


@pytest.mark.skip('Fix: Trigger for datetime update is not applied in test DB')
@pytest.mark.django_db
def test_updated_at_exception(
    debug_reporter: SQLReporter,
) -> None:
    """Test the exception on update created_at field."""
    # Setup
    before_time = timezone.now() - timedelta(days=1)
    MathExercise.objects.create(
        name='name',
        created_at=before_time,
        updated_at=before_time,
    )

    # Act
    debug_reporter.start_act()
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE math_exercise
                    SET name = %s, created_at = %s, updated_at = %s
                    WHERE name = %s
                """,
                    ('rename', before_time, before_time, 'name'),
                )
            debug_reporter.end_act()

    # Assert
    obj = MathExercise.objects.get(name='name')
    assert obj.updated_at != before_time
    assert obj.created_at == before_time
    assert abs((obj.created_at - timezone.now()).total_seconds()) < 1.0
