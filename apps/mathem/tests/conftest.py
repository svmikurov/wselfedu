"""Test configuration."""

import pytest

from typing import TypedDict

from rest_framework.test import APIClient, APIRequestFactory

class TaskRequestDict(TypedDict):
    """Type for top-level configuration dictionary."""

    name: str
    config: dict[str, int]


@pytest.fixture
def api_client() -> APIClient:
    """API client fixture."""
    return APIClient()


@pytest.fixture
def request_factory() -> APIRequestFactory:
    """Get return factory."""
    return APIRequestFactory()
