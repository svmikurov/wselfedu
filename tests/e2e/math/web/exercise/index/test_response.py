"""Exercise index page response tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from django.urls import reverse_lazy

if TYPE_CHECKING:
    from django.test import Client

URL_PATH = reverse_lazy('math:math_exercises')


class TestResponseCodeStatus:
    """Exercise index page response status code tests."""

    def test_get_method_response_success(self, client: Client) -> None:
        """Test GET method response status is OK."""
        # Act
        response = client.get(URL_PATH)
        # Assert
        assert response.status_code == HTTPStatus.OK
