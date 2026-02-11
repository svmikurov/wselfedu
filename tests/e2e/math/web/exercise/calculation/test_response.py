"""Calculation exercise page response tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse_lazy

if TYPE_CHECKING:
    from django.test import Client

REGULAR_URL_PATH = reverse_lazy('math:regular_calculation_exercise')


class TestRegularResponseCodeStatus:
    """Regular calculation exercise page response status code tests."""

    def test_get_method_response_anonymous(self, client: Client) -> None:
        """Test GET method response redirect for anonymous."""
        # Act
        response = client.get(REGULAR_URL_PATH)
        # Assert
        assert response.status_code == HTTPStatus.FOUND

    @pytest.mark.django_db
    def test_get_method_response_success(self, auth_client: Client) -> None:
        """Test GET method response code status is OK."""
        # Arrange
        params = {
            'min_operand': '1',
            'max_operand': '9',
            'operation_type': 'add',
        }
        # Act
        response = auth_client.get(REGULAR_URL_PATH, params)
        # Assert
        assert response.status_code == HTTPStatus.OK


@pytest.mark.skip('Implement detail view')
class TestDetailResponseCodeStatus:
    """Detail calculation exercise page response status code tests."""

    def test_get_method_response_success(self, client: Client) -> None:
        """Test GET method response status is OK."""
