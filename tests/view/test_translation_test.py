"""Translation test exercise view tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from apps.lang.views.exercise.translation.test import (
    RegularTranslationTestPerformView,
)

if TYPE_CHECKING:
    from django.core.handlers.wsgi import WSGIRequest

    from apps.lang.di.handler.web.container import WebHandlerContainer


@pytest.mark.django_db
def test_create_task_case(
    request_get_method: WSGIRequest,
    handlers: WebHandlerContainer,
    mock_create_exercise_action_handler: Mock,
) -> None:
    """Test create test exercise with GET method request."""
    # Act
    with handlers.regular_translation_test.override(  # type: ignore[unused-ignore]
        mock_create_exercise_action_handler,
    ):
        response = RegularTranslationTestPerformView.as_view()(
            request_get_method,
        )

    # Assert
    assert response.status_code == HTTPStatus.OK
