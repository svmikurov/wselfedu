"""Language discipline translation presentation exercise DI tests."""

import pytest

from di import MainContainer
from interfaces.schemas.domain.exercise import TaskItem

from .._types.handler import (
    HandlerT,
    RequestContextT,
    RequestDataT,
    RequestParamsT,
)

# =================================================
# Fixtures
# =================================================


@pytest.fixture
def regular_presentation_handler(main_container: MainContainer) -> HandlerT:
    """Provide translation regular presentation exercise handler."""
    return (  # type: ignore
        main_container.lang.handlers.regular_translation_presentation()  # type: ignore
    )


# =================================================
# Tests
# =================================================


def test_handler_initialized(regular_presentation_handler: HandlerT) -> None:
    """Test that presentation exercise handle initialized."""
    assert regular_presentation_handler is not None


@pytest.mark.django_db
def test_create_new_case(
    translations: list[TaskItem],
    request_params: RequestParamsT,
    request_context: RequestContextT,
    request_data_create_task: RequestDataT,  # Create task request data
    regular_presentation_handler: HandlerT,
) -> None:
    """Test *create task* handler action completed successfully."""
    assert (
        regular_presentation_handler.execute(
            request_params,
            request_context,
            request_data_create_task,
        )
    ) is not None


@pytest.mark.django_db
def test_update_progress(
    translations: list[TaskItem],
    null_request_params: RequestParamsT,
    user_request_context: RequestContextT,
    update_progress_request_data: RequestDataT,  # Update progress request data
    regular_presentation_handler: HandlerT,
) -> None:
    """Test *update progress* handler action completed successfully."""
    assert (
        regular_presentation_handler.execute(
            null_request_params,
            user_request_context,
            update_progress_request_data,
        )
        is not None
    )
