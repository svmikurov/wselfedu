"""Contains tests of exercise tables with ORM and SQL queries."""

from datetime import timedelta
from typing import Type

import pytest
from django.db import connection
from django.utils import timezone

from apps.lang.models import LangExercise
from apps.math.models import MathExercise

EXERCISES = (
    'schema, exercise',
    [
        ('math', MathExercise),
        ('lang', LangExercise),
    ],
)
INITIAL_NAME = 'initial exercise name'
UPDATED_NAME = 'updated exercise name'
TOLERANCE = timedelta(seconds=1)


@pytest.mark.parametrize(*EXERCISES)
@pytest.mark.django_db
def test_create_exercise_with_sql(
    schema: str,
    exercise: Type[MathExercise],
) -> None:
    """Test the auto-fill timestamp on create with row SQL.

    Test that the current datetime are set in the fild:
        - created_at
        - updated_at
    """
    # Set current datetime
    now = timezone.now()

    # Create exercise
    with connection.cursor() as cursor:
        cursor.execute(
            f'INSERT INTO {schema}.exercise (name) VALUES (%s)',
            (INITIAL_NAME,),
        )

    # Exercise created
    obj = exercise.objects.get(name=INITIAL_NAME)

    # The current datetime was set in the created_at field
    assert abs(obj.updated_at - now) < TOLERANCE

    # The current datetime was set in the updated_at field
    assert abs(obj.created_at - now) < TOLERANCE


@pytest.mark.parametrize(*EXERCISES)
@pytest.mark.django_db
def test_create_exercise_with_orm(
    schema: str,
    exercise: Type[MathExercise],
) -> None:
    """Test the auto-fill timestamp on create with ORM.

    Test that the current datetime are set in the fild:
        - created_at
        - updated_at
    """
    # Set current datetime
    now = timezone.now()

    # Create exercise
    exercise.objects.create(name=INITIAL_NAME)

    # Exercise created
    obj = exercise.objects.get(name=INITIAL_NAME)

    # The current datetime was set in the created_at field
    assert abs(obj.created_at - now) < TOLERANCE

    # The current datetime was set in the updated_at field
    assert abs(obj.updated_at - now) < TOLERANCE


@pytest.mark.parametrize(*EXERCISES)
@pytest.mark.django_db
def test_update_exercise_with_sql(
    schema: str,
    exercise: Type[MathExercise],
) -> None:
    """Test the auto-fill timestamp on update with row SQL.

    Test that the current datetime are set in the fild:
        - updated_at

    Test that the current datetime are NOT set in the fild:
        - created_at
    """
    # Set exercise
    obj = exercise.objects.create(name=INITIAL_NAME)

    # Update exercise name
    with connection.cursor() as cursor:
        cursor.execute(
            f'UPDATE {schema}.exercise SET name = %s WHERE name = %s',
            (UPDATED_NAME, INITIAL_NAME),
        )

    # Exercise updated
    updated_obj = exercise.objects.get(name=UPDATED_NAME)
    assert updated_obj.id == obj.id

    # The current datetime was NOT set in the created_at field
    assert updated_obj.created_at != updated_obj.updated_at


@pytest.mark.parametrize(*EXERCISES)
@pytest.mark.django_db
def test_update_exercise_with_orm(
    schema: str,
    exercise: Type[MathExercise],
) -> None:
    """Test the auto-fill timestamp on update with ORM request.

    Test that the current datetime are set in the fild:
        - updated_at

    Test that the current datetime are NOT set in the fild:
        - created_at
    """
    # Set exercise
    obj = exercise.objects.create(name=INITIAL_NAME)

    # Update exercise name
    exercise.objects.filter(name=INITIAL_NAME).update(name=UPDATED_NAME)

    # Exercise updated
    updated_obj = exercise.objects.get(name=UPDATED_NAME)
    assert updated_obj.id == obj.id

    # The current datetime was NOT set in the created_at field
    assert updated_obj.created_at != updated_obj.updated_at
