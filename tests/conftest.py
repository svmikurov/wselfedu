"""Test configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
from rest_framework.test import APIClient, APIRequestFactory

from apps.core.di.configuration import ExerciseConfig
from apps.core.domains.exercise import DisplayOrder
from di import MainContainer

if TYPE_CHECKING:
    from django.test import Client

    from apps.users.models import Person


pytest_plugins = [
    'tests.fixtures.user',
    'tests.fixtures.lang.db.case',
    'tests.fixtures.lang.db.assignment',
    'tests.fixtures.lang.db.parameters',
    'tests.fixtures.lang.db.translations',
    'tests.unit.lang.fixtures',
]


@pytest.fixture
def auth_client(user: Person, client: Client) -> Client:
    """Get main DI container."""
    client.force_login(user)
    return client


@pytest.fixture
def api_request_factory() -> APIRequestFactory:
    """Get API request factory."""
    return APIRequestFactory()


@pytest.fixture
def api_client() -> APIClient:
    """Get API client."""
    return APIClient()


# Mocking
# -------


@pytest.fixture
def mock_request(
    mock_user: Mock,
) -> Mock:
    """Mock request fixture."""
    request = Mock()
    request.user = mock_user
    return request


# DI


@pytest.fixture
def container() -> MainContainer:
    """Get main DI container."""
    return MainContainer()


@pytest.fixture
def exercise_configuration() -> ExerciseConfig:
    """Exercise configuration."""
    return ExerciseConfig(
        option_count=7,
        item_count=100,
        display_order=DisplayOrder.DEFINE,
    )
