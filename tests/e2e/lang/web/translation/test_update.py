"""Update english translation e2e tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from apps.lang import models

if TYPE_CHECKING:
    from django.test import Client

    from apps.users.models import Person

UPDATE_PATH_NAME = 'lang:english_translation_update'


@pytest.mark.django_db
class TestUpdateEnglishTranslation:
    """Update english translation tests."""

    def test_get_method_success(
        self,
        user: Person,
        client: Client,
        translation: models.EnglishTranslation,
    ) -> None:
        """Update translation GET method."""
        # Arrange
        client.force_login(user)
        update_url = reverse(UPDATE_PATH_NAME, kwargs={'pk': translation.pk})

        # Act
        response = client.get(update_url)

        # Assert
        # - status code
        assert response.status_code == HTTPStatus.OK

        # - the form is present in the context
        assert 'form' in response.context
        form = response.context['form']

        # - fields has words to update
        assert form['native'].value() == 'привет'
        assert form['foreign'].value() == 'hello'

    def test_post_method_success(
        self,
        user: Person,
        client: Client,
        translation: models.EnglishTranslation,
    ) -> None:
        """Update translation POST method."""
        # Arrange
        client.force_login(user)
        update_url = reverse(UPDATE_PATH_NAME, kwargs={'pk': translation.pk})
        form_data = {'native': 'привет', 'foreign': 'hi'}

        # Act
        response = client.post(update_url, data=form_data, follow=True)

        # Assert
        # - status code
        assert response.status_code == HTTPStatus.OK

        # - translated word has been updated
        updated = models.EnglishTranslation.objects.get(pk=translation.pk)
        assert updated.foreign.word == 'hi'


@pytest.mark.django_db
class TestPermissions:
    """Test update translation permissions."""

    def test_get_method_ownership(
        self,
        user_not_owner: Person,
        client: Client,
        translation: models.EnglishTranslation,
    ) -> None:
        """Ownership is required to receive the update form."""
        # Arrange
        client.force_login(user_not_owner)
        update_url = reverse(UPDATE_PATH_NAME, kwargs={'pk': translation.pk})

        # Act
        response = client.get(update_url)

        # Assert
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_post_method_ownership(
        self,
        user: Person,
        user_not_owner: Person,
        client: Client,
        translation: models.EnglishTranslation,
    ) -> None:
        """Ownership is required to update the translation."""
        # Arrange
        client.force_login(user_not_owner)
        update_url = reverse(UPDATE_PATH_NAME, kwargs={'pk': translation.pk})
        form_data = {'native': 'привет', 'foreign': 'hi'}

        # Act
        response = client.post(update_url, data=form_data)

        # Assert
        assert response.status_code == HTTPStatus.FORBIDDEN

        # - the translation has not been updated
        original = models.EnglishTranslation.objects.get(pk=translation.pk)
        assert original.foreign.word == 'hello'
        assert original.foreign.word != 'hi'
        assert original.user == user
        assert original.native.word == 'привет'
