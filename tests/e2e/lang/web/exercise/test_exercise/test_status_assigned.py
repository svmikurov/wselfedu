"""Assigned translation test exercise tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from apps.lang.models import EnglishAssignedExercise

if TYPE_CHECKING:
    from django.test import Client


class TestAssignedTranslationTestExercise:
    """Assigned translation test exercise tests."""

    @pytest.mark.django_db
    def test_get_method_response_status_ok(
        self,
        auth_client: Client,
        assignment: EnglishAssignedExercise,
    ) -> None:
        """Test response status OK."""
        # Arrange
        url_path = reverse(
            'lang:translation_english_test_mentorship',
            kwargs={'pk': assignment.pk},
        )

        # Act & Assert
        assert auth_client.get(url_path).status_code == HTTPStatus.OK

    @pytest.mark.django_db
    def test_post_method_response_status_ok(
        self,
        auth_client: Client,
        assignment: EnglishAssignedExercise,
    ) -> None:
        """Test response status OK."""
        # Arrange
        url_path = reverse(
            'lang:translation_english_test_mentorship',
            kwargs={'pk': assignment.pk},
        )

        # Act & Assert
        assert auth_client.post(url_path).status_code == HTTPStatus.OK
