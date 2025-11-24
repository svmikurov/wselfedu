"""Test configuration."""

from unittest.mock import Mock

import pytest
from rest_framework.test import APIClient, APIRequestFactory

from di import MainContainer

pytest_plugins = [
    'tests.fixtures.user',
    'tests.fixtures.lang.no_db.params_data',
    'tests.unit.lang.fixtures',
]


@pytest.fixture
def container() -> MainContainer:
    """Get main DI container."""
    return MainContainer()


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
