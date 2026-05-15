"""Translation presentation exercise WEB request tests."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Generic, TypeVar
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

if TYPE_CHECKING:
    from django.test import Client, RequestFactory

    from apps.users.models import Person

    from ._types import PresentationHandlerT

ParamsT = TypeVar('ParamsT')


@dataclass(frozen=True)
class RequestParams(Generic[ParamsT]):
    """Handler request parameters data."""

    params: ParamsT
    context: RequestContext
    data: RequestData[dict[str, Any]]


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
            response = auth_client.post(self.url)

            # Assert
            assert response.status_code == HTTPStatus.OK


# =================================================
# Prepare request parameters
# =================================================


class TestPresentationExerciseRequestParameters:
    """Presentation exercise web request parameters for presentation.

    Prepare request parameters for presentation handler.
    """

    @pytest.mark.parametrize(
        'data',
        (
            {
                'action': ExerciseAction.CREATE_TASK,
            },
        ),
    )
    def test_start_handler_request_parameters(
        self,
        data: dict[str, Any],
        user_schema: Person,
        mock_handler: Mock,
        request_factory: RequestFactory,
    ) -> None:
        """Test the request parameters for start handler.

        GET method.
        """
        # Arranger
        request_params = RequestParams(
            params=NullDTO(),
            context=RequestContext(user=user_schema, is_htmx=False),
            data=RequestData(data=data),
        )

        view = TranslationPresentationView()
        view.user = user_schema
        view._handler = mock_handler

        request = request_factory.get('/')
        view.request = request

        # Act
        view.get(request)

        # Assert
        call_args = mock_handler.execute.call_args

        mock_handler.execute.assert_called_once()

        # - that handler calls with correct attributes for action
        assert call_args.kwargs['params'] == request_params.params
        assert call_args.kwargs['context'] == request_params.context
        assert call_args.kwargs['data'] == request_params.data

    @pytest.mark.parametrize(
        'data',
        (
            {
                'action': ExerciseAction.CREATE_TASK,
            },
        ),
    )
    def test_process_handler_request_parameters(
        self,
        data: dict[str, Any],
        user_schema: Person,
        mock_handler: Mock,
        request_factory: RequestFactory,
    ) -> None:
        """Test the request parameters for start handler.

        POST method.
        """
        # Arranger
        expected_args = RequestParams(
            params=NullDTO(),
            context=RequestContext(user=user_schema, is_htmx=True),
            data=RequestData(data=data),
        )

        view = TranslationPresentationView()
        view.user = user_schema
        view._handler = mock_handler

        request = request_factory.post('/', headers={'HX-Request': 'true'})
        view.request = request

        # Act
        view.get(request)

        # Assert
        call_args = mock_handler.execute.call_args

        mock_handler.execute.assert_called_once()

        # - that handler calls with correct attributes for action
        assert call_args.kwargs['params'] == expected_args.params
        assert call_args.kwargs['context'] == expected_args.context
        assert call_args.kwargs['data'] == expected_args.data
