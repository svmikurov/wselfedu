"""Language discipline translation study context tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from apps.lang import models

if TYPE_CHECKING:
    from django.test import Client

    from apps.users.models import Person

URL_PATH = reverse('lang:translation_english_study_case')


@pytest.mark.django_db
class TestContext:
    """Translation study render context tests."""

    def test_info(
        self,
        user: Person,
        client: Client,
        english_progress: models.EnglishProgress,
    ) -> None:
        """Translation info test."""
        # Arrange
        client.force_login(user)

        # Act
        response = client.get(URL_PATH)

        # Assert
        assert 'info' in response.context.keys()
        info = response.context.get('info')

        assert info is not None
        assert info.get('progress') == english_progress.progress
