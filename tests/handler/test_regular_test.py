"""Language discipline translation test exercise DI tests."""

import pytest

from interfaces.schemas.domain.exercise import TaskItem

from .._types.handler import (
    HandlerT,
    RequestContextT,
    RequestDataT,
    RequestParamsT,
)


def test_handler_initialized(regular_test_handler: HandlerT) -> None:
    """Test that test exercise handle initialized."""
    assert regular_test_handler is not None


@pytest.mark.django_db
def test_create_new_case(
    translations: list[TaskItem],
    request_params: RequestParamsT,
    request_context: RequestContextT,
    request_data_create_task: RequestDataT,  # Create task request data
    regular_test_handler: HandlerT,
) -> None:
    """Test *create task* handler action completed successfully."""
    assert (
        regular_test_handler.execute(
            request_params,
            request_context,
            request_data_create_task,
        )
    ) is not None


@pytest.mark.django_db
def test_check_test_answer(
    translations: list[TaskItem],
    request_params: RequestParamsT,
    request_context: RequestContextT,
    request_data_check_test_answer: RequestDataT,  # Create task request data
    regular_test_handler: HandlerT,
) -> None:
    """Test *check answer* handler action completed successfully."""
    assert (
        regular_test_handler.execute(
            request_params,
            request_context,
            request_data_check_test_answer,
        )
    ) is not None
