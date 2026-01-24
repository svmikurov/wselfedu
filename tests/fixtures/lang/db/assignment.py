"""Exercise asignment fixtures."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from apps.core import models as core_models
from apps.lang import models as lang_models
from apps.users import models as users_models

if TYPE_CHECKING:
    from apps.users.models import Person


@pytest.fixture
def assignment(user: Person) -> lang_models.EnglishAssignedExercise:
    """Provide exercise assignment from mentor."""
    mentor = users_models.Person.objects.create_user(
        username='mentor',
        password='password',
    )
    mentorship = users_models.Mentorship.objects.create(
        mentor=mentor, student=user
    )
    exercise = lang_models.Exercise.objects.create(
        user=mentor,
        discipline=core_models.Discipline.objects.create(name='English'),
        name='translations',
    )
    assignment = lang_models.EnglishAssignedExercise.objects.create(
        mentorship=mentorship, exercise=exercise
    )
    return assignment
