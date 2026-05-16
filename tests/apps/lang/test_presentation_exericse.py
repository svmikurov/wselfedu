"""Translation presentation exercise WEB request tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
from django.urls import reverse_lazy

from apps.lang.views import TranslationPresentationView
from ports.contract.enums import ExerciseAction
from ports.interfaces.schemas.base import NullDTO
from ports.interfaces.schemas.request.handler import (
    RequestContext,
    RequestData,
)
from ports.interfaces.typed.web.exercise import TypedCreateTask

from ._types import RequestArgs

if TYPE_CHECKING:
    from django.test import Client, RequestFactory

    from apps.users.models import Person
    from ports.interfaces.typed.web.exercise import PresentationActionDataU

    from ._types import PresentationHandlerT


@pytest.fixture
def view(
    person_schema: Person,
    mock_handler: Mock,
) -> TranslationPresentationView:
    """Provide translation presentation view."""
    view = TranslationPresentationView()
    view.user = person_schema
    view._handler = mock_handler
    return view


@pytest.mark.django_db
class TestPresentationExerciseRequest:
    """Presentation exercise web request tests.

    Django integration request methods tests.
    """

    url = reverse_lazy('lang:translation_english_study')

    def test_get_method(
        self,
        auth_client: Client,
        regular_translation_presentation: PresentationHandlerT,
        mock_handler: Mock,
    ) -> None:
        """Test the GET request method."""
        # Act
        with regular_translation_presentation.override(mock_handler):  # type: ignore
            response = auth_client.get(self.url)

            # Assert
            mock_handler.execute.assert_called_once()
            assert response.status_code == HTTPStatus.OK

    def test_post_method(
        self,
        auth_client: Client,
        regular_translation_presentation: PresentationHandlerT,
        mock_handler: Mock,
    ) -> None:
        """Test the POST request method."""
        # Act
        with regular_translation_presentation.override(mock_handler):  # type: ignore
            response = auth_client.post(
                self.url,
                headers={'HX-Request': 'true'},
            )

            # Assert
            mock_handler.execute.assert_called_once()
            assert response.status_code == HTTPStatus.OK


class TestPresentationExerciseRequestParameters:
    """Presentation exercise web request parameters for presentation.

    Prepare request parameters for presentation handler.
    """

    def test_start_handler_request_parameters(
        self,
        person_schema: Person,
        mock_handler: Mock,
        view: TranslationPresentationView,
        request_factory: RequestFactory,
    ) -> None:
        """Test the request parameters for start handler.

        GET method for start exercise and initial template rendering.
        """
        # Arranger
        expected_args = RequestArgs(
            params=NullDTO(),
            context=RequestContext(user=person_schema),
            data=RequestData(data={'action': ExerciseAction.CREATE_TASK}),
        )

        request = request_factory.get('')
        view.request = request

        # Act
        view.get(request)

        # Assert
        mock_handler.execute.assert_called_once()

        call_args = mock_handler.execute.call_args
        assert call_args.kwargs['params'] == expected_args.params
        assert call_args.kwargs['context'] == expected_args.context
        assert call_args.kwargs['data'] == expected_args.data

    @pytest.mark.parametrize(
        'data',
        (
            TypedCreateTask(
                action=ExerciseAction.CREATE_TASK,
            ),
        ),
    )
    def test_process_handler_request_parameters(
        self,
        data: PresentationActionDataU,
        person_schema: Person,
        mock_handler: Mock,
        view: TranslationPresentationView,
        request_factory: RequestFactory,
    ) -> None:
        """Test the request parameters for start handler.

        POST method for exercise loop nad partial template rendering.
        """
        # Arranger
        expected_args = RequestArgs(
            params=NullDTO(),
            context=RequestContext(user=person_schema, is_htmx=True),
            data=RequestData(data=data),
        )

        request = request_factory.post(
            '',
            data=data,
            headers={'HX-Request': 'true'},
        )
        view.request = request

        # Act
        view.post(request)

        # Assert
        mock_handler.execute.assert_called_once()

        call_args = mock_handler.execute.call_args
        assert call_args.kwargs['params'] == expected_args.params
        assert call_args.kwargs['context'] == expected_args.context
        assert call_args.kwargs['data'] == expected_args.data
