"""Create translation view tests."""

from http import HTTPStatus
from unittest.mock import Mock

import pytest
from django.test import RequestFactory

import di
from apps.lang import views
from apps.lang.repositories.abc import TranslationRepoABC
from apps.users.models import Person


class TestCreateTranslationView:
    """Create translation view tests."""

    @pytest.mark.django_db
    def test_create_translation(self) -> None:
        """Repository create translation method was called."""
        # Arrange
        mock_user = Mock(spec=Person)
        mock_repo = Mock(spec=TranslationRepoABC)

        form_data = {
            'native': 'native text',
            'english': 'english text',
        }

        expected_call = {  # type: ignore[var-annotated]
            'native': 'native text',
            'english': 'english text',
            'category': None,
            'source': None,
            'user': mock_user,
            'marks': [],
        }

        request = RequestFactory().post('', data=form_data)
        request.user = mock_user

        # Act
        with di.container.lang.translation_repository.override(mock_repo):
            response = views.EnglishTranslationCreateView.as_view()(request)

        # Assert
        assert response.status_code == HTTPStatus.FOUND
        mock_repo.create.assert_called_once_with(**expected_call)
