"""Language discipline translation study response status tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from apps.lang import models

if TYPE_CHECKING:
    from django.test import Client


STUDY_URL = reverse('lang:translation_english_study')
STUDY_CASE_URL = reverse('lang:translation_english_study_case')


@pytest.mark.django_db
class TestStudyStatus:
    """Translation study request status tests."""

    def test_success_study_template(self, auth_client: Client) -> None:
        """No translation to study test."""
        # Act & Assert
        assert auth_client.get(STUDY_URL).status_code == HTTPStatus.OK

    def test_no_translation(self, auth_client: Client) -> None:
        """No translation to study test."""
        # Act & Assert
        assert auth_client.get(STUDY_URL).status_code == HTTPStatus.OK

    def test_anonymous(
        self,
        client: Client,
        translations: list[models.EnglishTranslation],
    ) -> None:
        """Anonymous request test."""
        # Act & Assert
        assert client.get(STUDY_URL).status_code == HTTPStatus.FOUND


@pytest.mark.django_db
class TestStudyCaseStatus:
    """Translation study case request status tests."""

    def test_success_study_case(
        self,
        auth_client: Client,
        translations: list[models.EnglishTranslation],
    ) -> None:
        """Status code success."""
        # Act & Assert
        assert auth_client.post(STUDY_CASE_URL).status_code == HTTPStatus.OK

    def test_no_translation(self, auth_client: Client) -> None:
        """No translation to study test."""
        # Act & Assert
        assert auth_client.post(STUDY_CASE_URL).status_code == HTTPStatus.OK

    def test_anonymous(
        self,
        client: Client,
        translations: list[models.EnglishTranslation],
    ) -> None:
        """Anonymous request test."""
        # Act & Assert
        assert (
            client.post(STUDY_CASE_URL).status_code == HTTPStatus.UNAUTHORIZED
        )
