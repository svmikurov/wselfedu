"""Create english translation e2e tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from apps.lang import models

if TYPE_CHECKING:
    from django.test import Client

    from apps.users.models import Person

CREATE_PATH_NAME = 'lang:translation_english_create'


@pytest.mark.django_db
class TestCreate:
    """Create english translation tests."""

    def test_get_method_success(self, user: Person, client: Client) -> None:
        """Create translation GET method."""
        # Arrange
        client.force_login(user)

        # Act
        response = client.get(reverse(CREATE_PATH_NAME))

        # Assert
        # - status code is 200
        assert response.status_code == HTTPStatus.OK

        # - the form is present in the context
        assert 'form' in response.context
        form = response.context['form']

        # - fields are empty
        assert form['native'].value() is None
        assert form['english'].value() is None

        # - the form is not bound to data
        assert not form.is_bound
        assert form.data == {}

        # - the form has no initial values
        assert form.initial == {}

    def test_post_method_success(self, user: Person, client: Client) -> None:
        """Create english translation POST method."""
        # Arrange
        client.force_login(user)
        initial_count = models.EnglishTranslation.objects.count()
        form_data = {'native': 'привет', 'english': 'hello'}

        # Act
        response = client.post(
            reverse(CREATE_PATH_NAME),
            data=form_data,
            follow=True,
        )

        # Assert
        # - status code
        assert response.status_code == HTTPStatus.OK

        # - the number of translation has increased
        assert models.EnglishTranslation.objects.count() == initial_count + 1

        # - translation has correct words
        translation = models.EnglishTranslation.objects.filter(
            native__word='привет'
        ).first()
        assert translation is not None
        assert translation.english.word == 'hello'

        # - redirect success
        assert response.resolver_match.view_name == CREATE_PATH_NAME


@pytest.mark.django_db
class TestPermissions:
    """Test create translation permissions."""

    def test_get_method_anonymous(self, client: Client) -> None:
        """Authorization is required to receive the translation form."""
        # Act
        response = client.get(reverse(CREATE_PATH_NAME))

        # Assert
        assert response.status_code == HTTPStatus.FOUND

    def test_post_method_anonymous(self, client: Client) -> None:
        """Authorization is required to add a translation."""
        # Arrange
        form_data = {'native': 'привет', 'english': 'hello'}

        # Act
        response = client.post(reverse(CREATE_PATH_NAME), data=form_data)

        # Assert
        assert response.status_code == HTTPStatus.FOUND
