"""Create translation view tests."""

from http import HTTPStatus
from unittest.mock import Mock

from django.test import RequestFactory

import di
from apps.lang import views
from apps.lang.repos.abc import TranslationRepoABC
from apps.users.models import Person


class TestCreateTranslationView:
    """Create translation view tests."""

    def test_create_translation_success(self) -> None:
        """Translation was created successfully."""
        # Arrange
        mock_user = Mock(spec=Person)
        mock_repo = Mock(spec=TranslationRepoABC)

        form_data = {
            'native': 'native text',
            'english': 'english text',
        }

        request = RequestFactory().post('', data=form_data)
        request.user = mock_user

        # Act
        with di.container.lang.translation_repo.override(mock_repo):
            response = views.EnglishTranslationCreateView.as_view()(request)

        # Assert
        assert response.status_code == HTTPStatus.FOUND
        mock_repo.create_translation.assert_called_once_with(
            mock_user, **form_data
        )
