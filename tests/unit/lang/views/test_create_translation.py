"""Create translation view tests."""

from http import HTTPStatus
from typing import Any
from unittest.mock import Mock

import pytest
from django.test import RequestFactory

import di
from apps.lang import views
from apps.lang.repos.abc import TranslationRepoABC
from apps.users.models import Person


@pytest.fixture
def form_data() -> dict[str, Any]:
    """Provide request form data."""
    return {
        'native': 'native text',
        'english': 'english text',
    }


class TestCreateTranslationView:
    """Create translation view tests."""

    def test_create_translation(
        self,
        form_data: dict[str, Any],
    ) -> None:
        """Test via request factory the translation creation."""
        # Arrange
        mock_user = Mock(spec=Person)
        mock_repo = Mock(spec=TranslationRepoABC)

        request = RequestFactory().post('', data=form_data)
        request.user = mock_user

        # Act
        with di.container.lang.translation_repo.override(mock_repo):
            response = views.EnglishTranslationCreateView.as_view()(request)

        # Assert
        assert response.status_code == HTTPStatus.FOUND
        mock_repo.create_translation.assert_called_once_with(
            user=mock_user,
            **form_data,
        )
