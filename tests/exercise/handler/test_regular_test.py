"""Language discipline translation test exercise DI tests."""

import pytest

from interfaces.schemas.domain.exercise import TaskItem
from tests.types.handler import (
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
    request_params: RequestParamsT,
    request_context: RequestContextT,
    create_task_request_data: CreateRequestDataT,
    regular_test_handler: HandlerT,
) -> None:
    """Test *create task* handler action completed successfully."""
    assert (
        regular_test_handler.execute(
            request_params,
            request_context,
            create_task_request_data,
        )
    ) is not None


@pytest.mark.django_db
def test_check_test_answer(
    translations: list[TaskItem],
    request_params: RequestParamsT,
    request_context: RequestContextT,
    check_test_answer_request_data: CheckRequestDataT,
    regular_test_handler: HandlerT,
) -> None:
    """Test *check answer* handler action completed successfully."""
    assert (
        regular_test_handler.execute(
            request_params,
            request_context,
            check_test_answer_request_data,
        )
    ) is not None
