"""Exercise page test."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
from django.urls import reverse

from tests.factories.mock import create_learnable_repo_mock
from wse.di import django_site_container

if TYPE_CHECKING:
    from django.test import Client

    from wse.domain.protocols import UniqueLearnable


@pytest.fixture
def mock_learnable_repo(learnables: tuple[UniqueLearnable, ...]) -> Mock:
    """Provide a learnable repository mock with added learnables."""
    return create_learnable_repo_mock(learnables)


@pytest.mark.usefixtures('mock_learnable_repo')
def test_exercise_page_returns_http_200(
    client: Client,
    mock_learnable_repo: Mock,
) -> None:
    # Arrange
    url = reverse('testing')

    # Act
    with django_site_container.use_cases.repositories.learnable.override(
        mock_learnable_repo
    ):
        response = client.get(url)

        # Assert
        assert response.status_code == HTTPStatus.OK
