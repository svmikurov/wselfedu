"""Test the view routes by "/calculation/" path."""

import json
from typing import Any

import pytest
from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from wse_exercises.core.mathem.base.exercise import SimpleMathTaskRequest
from wse_exercises.core.mathem.task import SimpleMathTask

from apps.mathem.api.v1.views import CalculationViewSet
from apps.mathem.tests.conftest import TaskRequestDict
from services.exercise import SimpleMathExerciseService

URL = '/api/v1/math/calculation/simple/'


@pytest.fixture
def viewset() -> CalculationViewSet:
    """Get view."""
    return CalculationViewSet()


@pytest.fixture
def task_request_data() -> TaskRequestDict:
    """Return data for requesting a task with a configuration."""
    return {
        'name': 'adding',
        'config': {
            'min_value': 1,
            'max_value': 9,
        },
    }


@pytest.fixture
def task_request_dto(
    task_request_data: TaskRequestDict,
) -> SimpleMathTaskRequest:
    """Return task request DTO."""
    return SimpleMathTaskRequest.model_validate(task_request_data)


@pytest.fixture
def task_data() -> dict[str, Any]:
    """Return task data."""
    return {
        'config': {'min_value': 1, 'max_value': 9},
        'conditions': {'operand_1': 4, 'operand_2': 3},
        'question': {'text': '4 + 3'},
        'answer': {'text': '7'},
        'exercise_name': 'adding',
    }


@pytest.fixture
def task_dto(task_data: dict[str, Any]) -> SimpleMathTask:
    """Return task DTO."""
    return SimpleMathTask.model_validate(task_data)


def test_response_status(
    client: APIClient,
    task_request_data: TaskRequestDict,
) -> None:
    """Test response status OK."""
    response = client.post(
        URL,
        data=task_request_data,
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_200_OK


def test_create_task_success(
    viewset: CalculationViewSet,
    request_factory: APIRequestFactory,
    task_request_data: TaskRequestDict,
    task_request_dto: SimpleMathTaskRequest,
    task_data: dict[str, Any],
    task_dto: SimpleMathTask,
    mocker: MockerFixture,
) -> None:
    """Test the view that the task was created successfully."""
    # Validate pydantic model
    SimpleMathTaskRequest.model_validate(task_request_data)

    # Mock create task service and its create task method
    mock_service = mocker.Mock(spec=SimpleMathExerciseService)
    mock_service.create_task.return_value = task_dto

    # Creating a request
    request = request_factory.post(
        URL,
        data=task_request_data,
        format='json',
    )

    # Wrapping in DRF Request
    drf_request = Request(request)

    # Adding a JSON parser
    drf_request.parsers = [JSONParser()]

    # Call viewset method
    response = viewset.render_task(  # type: ignore
        request=drf_request,
        exercise_service=mock_service,
    )

    # Assert that a method is called with the expected data.
    mock_service.create_task.assert_called_once_with(task_request_dto)

    # Assert that a method return expected value.
    response_data = json.loads(response.data)
    assert task_data.items() <= response_data.items()
