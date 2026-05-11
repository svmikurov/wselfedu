"""Language discipline translation test exercise DI tests.

Applies existing DI containers for dependency test.
"""

import pytest

from ports.interfaces.schemas.domain.exercise.exercise import TaskItem
from tests.legacy.types.handler import (
    HandlerT,
    RequestContextT,
    RequestParamsT,
)

from .._types import CheckRequestDataT, CreateRequestDataT


def test_handler_initialized(regular_test_handler: HandlerT) -> None:
    """Test that test exercise handle initialized."""
    assert regular_test_handler is not None


@pytest.mark.django_db
def test_create_new_case(
    translations: list[TaskItem],
    mock_request_params: RequestParamsT,
    request_context: RequestContextT,
    create_task_request_data: CreateRequestDataT,
    regular_test_handler: HandlerT,
) -> None:
    """Test *create task* handler action completed successfully."""
    assert (
        regular_test_handler.execute(
            mock_request_params,
            request_context,
            create_task_request_data,
        )
    ) is not None


@pytest.mark.django_db
def test_check_test_answer(
    translations: list[TaskItem],
    mock_request_params: RequestParamsT,
    request_context: RequestContextT,
    create_task_request_data: CreateRequestDataT,
    check_test_answer_request_data: CheckRequestDataT,
    regular_test_handler: HandlerT,
) -> None:
    """Test *check answer* handler action completed successfully."""
    # Arrange
    # - Save the current case for answer check.
    # HACK: Update the current case saving for test isolation.
    regular_test_handler.execute(
        mock_request_params,
        request_context,
        create_task_request_data,
    )

    # Act & assert
    assert (
        regular_test_handler.execute(
            mock_request_params,
            request_context,
            check_test_answer_request_data,
        )
        is not None
    )
