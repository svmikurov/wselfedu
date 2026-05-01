"""Translation presentation exercise view test."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from apps.lang.views.exercise.translation.presentation import (
    TranslationPresentationView,
)

if TYPE_CHECKING:
    from django.core.handlers.wsgi import WSGIRequest

    from apps.lang.di.handler.web.container import WebHandlerContainer


@pytest.mark.django_db
class TestTranslationPresentationView:
    """Translation presentation exercise view test."""

    def test_get_request_create_action(
        self,
        request_get_method: WSGIRequest,
        handlers: WebHandlerContainer,
        mock_create_exercise_action_handler: Mock,
    ) -> None:
        """Test GET request success with request handler mock."""
        # Act
        with handlers.process_regular_translation_presentation.override(  # type: ignore[unused-ignore]
            mock_create_exercise_action_handler,
        ):
            response = TranslationPresentationView.as_view()(
                request_get_method,
            )

        # Assert
        assert response.status_code == HTTPStatus.OK

    def test_post_request_create_action(
        self,
        request_post_method: WSGIRequest,
        handlers: WebHandlerContainer,
        mock_create_exercise_action_handler: Mock,
    ) -> None:
        """Test POST request success with request handler mock."""
        # Act
        with handlers.process_regular_translation_presentation.override(  # type: ignore[unused-ignore]
            mock_create_exercise_action_handler
        ):
            response = TranslationPresentationView.as_view()(
                request_post_method,
            )

        # Assert
        assert response.status_code == HTTPStatus.OK
