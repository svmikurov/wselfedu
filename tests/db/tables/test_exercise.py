"""Contains tests of exercise tables with ORM and SQL queries."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Type, Union

import pytest
from django.utils import timezone

from apps.core.models import Discipline
from apps.lang.models import Exercise
from apps.math.models import MathExercise

if TYPE_CHECKING:
    from apps.users.models import Person

    type ExerciseType = Union[Type[Exercise], Type[MathExercise]]

EXERCISES = (
    'schema, exercise',
    [
        ('math', MathExercise),
        ('lang', Exercise),
    ],
)
INITIAL_NAME = 'initial exercise name'
UPDATED_NAME = 'updated exercise name'
TOLERANCE = timedelta(seconds=1)

# HACK: Remove type condition in tests and type ignoring
# after adding user to mathematical exercise model


@pytest.fixture
def discipline() -> Discipline:
    """Fixture provides discipline model instance."""
    return Discipline.objects.create(name='Math')


@pytest.mark.parametrize(*EXERCISES)
@pytest.mark.django_db
def test_create_exercise(
    schema: str,
    exercise: ExerciseType,
    discipline: Discipline,
    user: Person,
) -> None:
    """Test the auto-fill timestamp on create with ORM.

    Test that the current datetime are set in the fild:
        - created_at
        - updated_at
    """
    # Set current datetime
    now = timezone.now()

    # Create exercise
    if exercise is Exercise:
        exercise.objects.create(  # type: ignore[misc]
            user=user, discipline=discipline, name=INITIAL_NAME
        )
    else:
        exercise.objects.create(discipline=discipline, name=INITIAL_NAME)

    # Exercise created
    obj = exercise.objects.get(name=INITIAL_NAME)

    # The current datetime was set in the created_at field
    assert abs(obj.created_at - now) < TOLERANCE

    # The current datetime was set in the updated_at field
    assert abs(obj.updated_at - now) < TOLERANCE


@pytest.mark.parametrize(*EXERCISES)
@pytest.mark.django_db
def test_update_exercise(
    schema: str,
    exercise: ExerciseType,
    discipline: Discipline,
    user: Person,
) -> None:
    """Test the auto-fill timestamp on update with ORM request.

    Test that the current datetime are set in the fild:
        - updated_at

    Test that the current datetime are NOT set in the fild:
        - created_at
    """
    # Set exercise
    if exercise is Exercise:
        obj = exercise.objects.create(  # type: ignore[misc]
            user=user, discipline=discipline, name=INITIAL_NAME
        )
    else:
        obj = exercise.objects.create(discipline=discipline, name=INITIAL_NAME)

    # Update exercise name
    exercise.objects.filter(name=INITIAL_NAME).update(name=UPDATED_NAME)

    # Exercise updated
    updated_obj = exercise.objects.get(name=UPDATED_NAME)
    assert updated_obj.id == obj.id

    # The current datetime was NOT set in the created_at field
    assert updated_obj.created_at != updated_obj.updated_at
