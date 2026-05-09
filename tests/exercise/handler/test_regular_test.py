"""Language discipline translation test exercise DI tests."""

from unittest.mock import Mock

import pytest

from contracts.enums import ExerciseStatus
from di import MainContainer
from interfaces.schemas.domain.exercise import (
    TaskItem,
    TestExerciseDomainResult,
)
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
    mock_user_command_storage: Mock,
    main_container: MainContainer,
) -> None:
    """Test *check answer* handler action completed successfully."""
    # Arrange
    mock_user_command_storage.retrieve.return_value = TestExerciseDomainResult(
        question_option_value=0,
        status=ExerciseStatus.NEW_TASK,
        items=translations,
    )

    # Act
    with main_container.lang.use_cases.user_command_storage.override(  # type: ignore[attr-defined]
        mock_user_command_storage
    ):
        handler = (
            main_container.lang.handlers.regular_translation_test()  # type: ignore[attr-defined]
        )
        result = handler.execute(
            request_params,
            request_context,
            check_test_answer_request_data,
        )

        # Assert
        assert result is not None
