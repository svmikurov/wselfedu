"""Contains tests of database table features."""

from datetime import timedelta

import pytest
from django.db import connection
from django.utils import timezone

from apps.math.models import MathExercise


@pytest.mark.django_db
def test_create_exercise_with_sql() -> None:
    """Test the auto-fill timestamp on create with row SQL.

    Test that the current datetime are set in the fild:
        - created_at
        - updated_at
    """
    test_name = 'raw_sql_creation_test'
    tolerance = timedelta(seconds=1)
    now = timezone.now()

    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO math.exercise (name) VALUES (%s)',
            (test_name,),
        )

    obj = MathExercise.objects.get(name=test_name)

    # Object created
    assert MathExercise.objects.filter(name=test_name).exists()

    # The current datetime was set in the created_at field
    assert abs(obj.updated_at - now) < tolerance

    # The current datetime was set in the updated_at field
    assert abs(obj.created_at - now) < tolerance


@pytest.mark.django_db
def test_created_exercise_with_orm() -> None:
    """Test the auto-fill timestamp on create with ORM.

    Test that the current datetime are set in the fild:
        - created_at
        - updated_at
    """
    test_name = 'raw_sql_creation_test'
    tolerance = timedelta(seconds=1)
    now = timezone.now()

    MathExercise.objects.create(name=test_name)

    obj = MathExercise.objects.get(name=test_name)

    # Object created
    assert MathExercise.objects.filter(name=test_name).exists()

    # The current datetime was set in the created_at field
    assert abs(obj.created_at - now) < tolerance

    # The current datetime was set in the updated_at field
    assert abs(obj.updated_at - now) < tolerance


@pytest.mark.django_db
def test_updated_exercise_with_sql() -> None:
    """Test the auto-fill timestamp on update with row SQL.

    Test that the current datetime are set in the fild:
        - updated_at

    Test that the current datetime are NOT set in the fild:
        - created_at
    """
    test_name = 'raw_sql_update_test'
    updated_name = 'raw_sql_updated_test'
    initial_time = timezone.now() - timedelta(days=1)

    obj = MathExercise.objects.create(
        name=test_name,
        created_at=initial_time,
        updated_at=initial_time,
    )
    with connection.cursor() as cursor:
        cursor.execute(
            'UPDATE math.exercise SET name = %s WHERE name = %s',
            (updated_name, test_name),
        )

    updated_obj = MathExercise.objects.get(name=updated_name)

    # Object updated
    assert not MathExercise.objects.filter(name=test_name).exists()
    assert MathExercise.objects.filter(name=updated_name).exists()
    assert updated_obj.id == obj.id

    # The current datetime was NOT set in the created_at field
    assert updated_obj.created_at == initial_time

    # The current datetime was set in the updated_at field
    assert updated_obj.updated_at > initial_time


@pytest.mark.django_db
def test_updated_exercise_with_orm() -> None:
    """Test the auto-fill timestamp on update with ORM request.

    Test that the current datetime are set in the fild:
        - updated_at

    Test that the current datetime are NOT set in the fild:
        - created_at
    """
    test_name = 'orm_update_test'
    updated_name = 'orm_updated_test'
    initial_time = timezone.now() - timedelta(days=1)

    obj = MathExercise.objects.create(
        name=test_name,
        created_at=initial_time,
        updated_at=initial_time,
    )

    MathExercise.objects.filter(name=test_name).update(name=updated_name)

    updated_obj = MathExercise.objects.get(name=updated_name)

    # Object updated
    assert not MathExercise.objects.filter(name=test_name).exists()
    assert MathExercise.objects.filter(name=updated_name).exists()
    assert updated_obj.id == obj.id

    # The current datetime was NOT set in the created_at field
    assert updated_obj.created_at == initial_time

    # The current datetime was set in the updated_at field
    assert updated_obj.updated_at != initial_time
