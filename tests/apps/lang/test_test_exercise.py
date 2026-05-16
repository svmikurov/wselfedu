"""Translation test exercise WEB request tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
from django.urls import reverse_lazy

from apps.lang.views import RegularTranslationTestPerformView
from ports.contract.enums import ExerciseAction
from ports.interfaces.request.web.exercise import (
    CheckTestRequestData,
    CreateTaskRequestData,
)
from ports.interfaces.schemas.base import NullDTO
from ports.interfaces.schemas.request.handler import (
    RequestContext,
    RequestData,
)

from ._types import RequestArgs

if TYPE_CHECKING:
    from django.test import Client, RequestFactory

    from apps.users.models import Person
    from ports.interfaces.request.web.exercise import TestActionDataU

    from ._types import TestHandlerT


@pytest.fixture
def view(
    person_schema: Person,
    mock_handler: Mock,
) -> RegularTranslationTestPerformView:
    """Provide translation presentation view."""
    view = RegularTranslationTestPerformView()
    view.user = person_schema
    view._handler = mock_handler
    return view


@pytest.mark.django_db
class TestTestExerciseRequest:
    """Test exercise WEB request tests.

    Django integration request methods tests.
    """

    url = reverse_lazy('lang:translation_english_test')

    def test_get_method(
        self,
        auth_client: Client,
        regular_translation_test: TestHandlerT,
        mock_handler: Mock,
    ) -> None:
        """Test the GET request method."""
        # Act
        with regular_translation_test.override(mock_handler):  # type: ignore
            response = auth_client.get(self.url)

            # Assert
            mock_handler.execute.assert_called_once()
            assert response.status_code == HTTPStatus.OK

    def test_post_method(
        self,
        auth_client: Client,
        regular_translation_test: TestHandlerT,
        mock_handler: Mock,
    ) -> None:
        """Test the POST request method."""
        # Act
        with regular_translation_test.override(mock_handler):  # type: ignore
            response = auth_client.post(
                self.url,
                headers={'HX-Request': 'true'},
            )

            # Assert
            mock_handler.execute.assert_called_once()
            assert response.status_code == HTTPStatus.OK


class TestTestExerciseRequestParameters:
    """Test exercise WEB request parameters for test exercise.

    Prepare request parameters for test exercise handler.
    """

    def test_start_handler_request_parameters(
        self,
        person_schema: Person,
        mock_handler: Mock,
        view: RegularTranslationTestPerformView,
        request_factory: RequestFactory,
    ) -> None:
        """Test the request parameters for start handler.

        GET method.
        """
        # Arranger
        expected_args = RequestArgs(
            params=NullDTO(),
            context=RequestContext(user=person_schema),
            data=RequestData(
                data=CreateTaskRequestData(action=ExerciseAction.CREATE_TASK)
            ),
        )

        request = request_factory.get('/')
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
            CreateTaskRequestData(
                action=ExerciseAction.CREATE_TASK,
            ),
            CheckTestRequestData(
                action=ExerciseAction.CHECK_ANSWER,
                option_value='3',
            ),
        ),
        ids=['create_task', 'check_answer_with_option'],
    )
    def test_process_handler_request_parameters(
        self,
        data: TestActionDataU,
        person_schema: Person,
        mock_handler: Mock,
        request_factory: RequestFactory,
    ) -> None:
        """Test the request parameters for start handler.

        POST method.
        """
        # Arranger
        expected_args = RequestArgs(
            params=NullDTO(),
            context=RequestContext(user=person_schema, is_htmx=True),
            data=RequestData(data=data),
        )

        view = RegularTranslationTestPerformView()
        view.user = person_schema
        view._handler = mock_handler

        request = request_factory.post(
            '/',
            data=data,
            headers={'HX-Request': 'true'},
        )
        view.request = request

        # Act
        view.post(request)

        print(f'{view.request.headers = }')

        # Assert
        mock_handler.execute.assert_called_once()

        call_args = mock_handler.execute.call_args
        assert call_args.kwargs['params'] == expected_args.params
        assert call_args.kwargs['context'] == expected_args.context
        assert call_args.kwargs['data'] == expected_args.data
