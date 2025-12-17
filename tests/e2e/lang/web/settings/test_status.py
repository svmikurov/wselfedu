"""Language discipline study settings response status tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

if TYPE_CHECKING:
    from django.test import Client

    from apps.users.models import Person

URL_PATH = reverse('lang:settings')


@pytest.mark.django_db
class TestStatusSimple:
    """Response status test."""

    def test_get_method_success(
        self,
        user: Person,
        client: Client,
    ) -> None:
        """GET method success status test."""
        # Arrange
        client.force_login(user)

        # Act
        response = client.get(URL_PATH)

        # Assert
        assert response.status_code == HTTPStatus.OK

    def test_post_method_success(
        self,
        user: Person,
        client: Client,
    ) -> None:
        """POST method success status test."""
        # Arrange
        client.force_login(user)

        # Act
        response = client.post(URL_PATH)

        # Assert
        assert response.status_code == HTTPStatus.OK
