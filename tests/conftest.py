"""Pytest configuration."""

from unittest.mock import Mock

import pytest

from apps.users.models import Person

pytest_plugins = [
    'tests.fixtures.db_user',
    'tests.fixtures.di',
    'tests.fixtures.exercise.request_data',
    'tests.fixtures.exercise.lang.db.params',
    'tests.fixtures.exercise.lang.db.translations',
    'tests.fixtures.exercise.lang.no_db.params',
]


@pytest.fixture
def mock_user() -> Person:
    """Provide user mock."""
    mock = Mock(spec=Person)
    mock.pk = 1
    return mock
