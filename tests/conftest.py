"""Pytest configuration."""

from unittest.mock import Mock

import pytest

from apps.core.repositories.protocol import RepositoryProtocol
from apps.lang.models import EnglishTranslation
from apps.lang.repositories.exercise import UserTranslationsRepository
from apps.users.models import Person
from contracts.schemas.domain.exercise import ExerciseParametersDTO

pytest_plugins = [
    'tests.fixtures.db_user',
    'tests.fixtures.di.container',
    'tests.fixtures.exercise.request_data',
    'tests.fixtures.exercise.lang.db.params',
    'tests.fixtures.exercise.lang.db.translations',
    'tests.fixtures.exercise.lang.no_db.params',
]


@pytest.fixture
def mock_user() -> Person:
    """Provide user mock."""
    return Mock(spec=Person)


# =================================================
# Exercise parameters
# =================================================


@pytest.fixture
def exercise_params() -> ExerciseParametersDTO:
    """Provide exercise parameters."""
    return ExerciseParametersDTO()


# =================================================
# Exercise data
# =================================================


@pytest.fixture
def translation_repository() -> RepositoryProtocol[object, object]:
    """Provide exercise config.."""
    return UserTranslationsRepository(
        manager=EnglishTranslation.objects,
    )
