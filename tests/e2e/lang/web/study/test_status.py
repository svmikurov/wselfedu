"""Language discipline translation study response status tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from apps.lang import models

if TYPE_CHECKING:
    from django.test import Client

    from apps.users.models import Person

STUDY_URL_PATH = reverse('lang:translation_english_study')
STUDY_CASE_URL_PATH = reverse('lang:translation_english_study_case')


@pytest.mark.django_db
class TestStudyStatus:
    """Translation study request status tests."""

    def test_success_study_template(
        self,
        user: Person,
        client: Client,
        translations: list[models.EnglishTranslation],
    ) -> None:
        """No translation to study test."""
        # Arrange
        client.force_login(user)

        # Act & Assert
        assert client.get(STUDY_URL_PATH).status_code == HTTPStatus.OK

    def test_no_translation(
        self,
        user: Person,
        client: Client,
    ) -> None:
        """No translation to study test."""
        # Arrange
        client.force_login(user)

        # Act & Assert
        assert client.get(STUDY_URL_PATH).status_code == HTTPStatus.OK

    def test_anonymous(
        self,
        client: Client,
        translations: list[models.EnglishTranslation],
    ) -> None:
        """Anonymous request test."""
        # Act & Assert
        assert client.get(STUDY_URL_PATH).status_code == HTTPStatus.FOUND


@pytest.mark.django_db
class TestStudyCaseStatus:
    """Translation study case request status tests."""

    def test_success_study_case(
        self,
        user: Person,
        client: Client,
        translations: list[models.EnglishTranslation],
    ) -> None:
        """No translation to study test."""
        # Arrange
        client.force_login(user)

        # Act & Assert
        assert client.get(STUDY_CASE_URL_PATH).status_code == HTTPStatus.OK

    def test_no_translation(
        self,
        user: Person,
        client: Client,
    ) -> None:
        """No translation to study test."""
        # Arrange
        client.force_login(user)

        # Act & Assert
        assert client.get(STUDY_CASE_URL_PATH).status_code == HTTPStatus.FOUND

    def test_anonymous(
        self,
        client: Client,
        translations: list[models.EnglishTranslation],
    ) -> None:
        """Anonymous request test."""
        # Act & Assert
        assert client.get(STUDY_CASE_URL_PATH).status_code == HTTPStatus.FOUND
