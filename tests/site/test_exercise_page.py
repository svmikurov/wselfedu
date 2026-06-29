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
def testing_exercise_url() -> str:
    """Provide a testing exercise url."""
    return reverse('testing')


@pytest.fixture
def mock_learnable_repo(learnables: tuple[UniqueLearnable, ...]) -> Mock:
    """Provide a learnable repository mock with added learnables."""
    return create_learnable_repo_mock(learnables)


@pytest.mark.django_db
def test_start_exercise_page_returns_http_200(
    client: Client,
    testing_exercise_url: str,
    mock_learnable_repo: Mock,
) -> None:
    # Act
    with django_site_container.use_cases.repositories.learnable.override(  # type: ignore
        mock_learnable_repo
    ):
        response = client.get(testing_exercise_url)

        # Assert
        assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_perform_exercise_page_returns_http_200(
    client: Client,
    testing_exercise_url: str,
    mock_learnable_repo: Mock,
) -> None:
    # Act
    with django_site_container.use_cases.repositories.learnable.override(  # type: ignore
        mock_learnable_repo
    ):
        response = client.post(
            testing_exercise_url, headers={'HX-Request': 'true'}
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
