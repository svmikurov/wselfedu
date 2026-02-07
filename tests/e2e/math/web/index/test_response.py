"""Mathematical discipline index page tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from django.urls import reverse_lazy

if TYPE_CHECKING:
    from django.test import Client

MATH_INDEX_PATH = reverse_lazy('math:index')


class TestResponseStatus:
    """Mathematical discipline index page tests."""

    def test_get_method_response_success(self, client: Client) -> None:
        """Test GET method response status is OK."""
        # Act
        response = client.get(MATH_INDEX_PATH)
        # Assert
        assert response.status_code == HTTPStatus.OK
