"""Delete english translation e2e tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from apps.lang import models

if TYPE_CHECKING:
    from django.test import Client

    from apps.users.models import Person

DELETE_PATH_NAME = 'lang:translation_english_delete'


@pytest.fixture
def remain_translation(user: Person) -> models.EnglishTranslation:
    """Get translation which remains after other word deletion."""
    return models.EnglishTranslation.objects.create(
        user=user,
        native=models.NativeWord.objects.create(user=user, word='слово'),
        english=models.EnglishWord.objects.create(user=user, word='word'),
    )


@pytest.mark.django_db
class TestDeleteEnglishTranslation:
    """Delete english translation tests."""

    def test_delete_method_success(
        self,
        user: Person,
        client: Client,
        translation: models.EnglishTranslation,
        remain_translation: models.EnglishTranslation,
    ) -> None:
        """Delete translation DELETE method."""
        # Arrange
        client.force_login(user)
        url = reverse(DELETE_PATH_NAME, kwargs={'pk': translation.pk})

        # Act
        response = client.delete(url)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert models.EnglishTranslation.objects.filter(user=user).count() == 1

    def test_delete_method_ownership(
        self,
        user: Person,
        user_not_owner: Person,
        client: Client,
        translation: models.EnglishTranslation,
        remain_translation: models.EnglishTranslation,
    ) -> None:
        """Delete translation ownership."""
        # Arrange
        client.force_login(user_not_owner)
        url = reverse(DELETE_PATH_NAME, kwargs={'pk': translation.pk})

        # Act
        response = client.delete(url)

        # Assert
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert models.EnglishTranslation.objects.filter(user=user).count() == 2

    def test_delete_method_anonymous(
        self,
        user: Person,
        client: Client,
        translation: models.EnglishTranslation,
        remain_translation: models.EnglishTranslation,
    ) -> None:
        """Delete translation by anonymous."""
        # Arrange
        url = reverse(DELETE_PATH_NAME, kwargs={'pk': translation.pk})

        # Act
        response = client.delete(url)

        # Assert
        assert response.status_code == HTTPStatus.FOUND
        assert models.EnglishTranslation.objects.filter(user=user).count() == 2
