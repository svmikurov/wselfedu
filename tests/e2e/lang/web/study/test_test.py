"""Translation study test exercise tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse_lazy

from apps.lang.schemas import CaseStatus

if TYPE_CHECKING:
    from django.test import Client

    from apps.lang import models

TRANSLATION_TEST_URL = reverse_lazy('lang:translation_english_test')


@pytest.mark.django_db
class TestHttpStatus:
    """Translation test exercise http status tests."""

    def test_render_template_success(
        self,
        auth_client: Client,
    ) -> None:
        """Translation test exercise http status is success."""
        # Act
        response = auth_client.get(TRANSLATION_TEST_URL)

        # Assert
        assert response.status_code == HTTPStatus.OK

    def test_request_case_success(
        self,
        auth_client: Client,
        translations: list[models.EnglishTranslation],
    ) -> None:
        """Translation test case http status is success."""
        # Arrange
        data = {'status': CaseStatus.NEW}

        # Act
        response = auth_client.post(TRANSLATION_TEST_URL, data=data)

        # Assert
        assert response.status_code == HTTPStatus.OK
