"""Language discipline translation presentation exercise DI tests.

Applies existing DI containers for dependency test.
"""

from unittest.mock import Mock

import pytest

from di import MainContainer
from ports.contract.enums import ExerciseStatus
from ports.interfaces.schemas.domain.exercise.exercise import (
    PresentationExerciseDomainResult,
    TaskItem,
)
from tests.legacy.types.handler import (
    HandlerT,
    RequestContextT,
    RequestDataT,
    RequestParamsT,
)


def test_handler_initialized(regular_presentation_handler: HandlerT) -> None:
    """Test that presentation exercise handle initialized."""
    assert regular_presentation_handler is not None


@pytest.mark.django_db
def test_create_new_case(
    translations: list[TaskItem],
    mock_request_params: RequestParamsT,
    request_context: RequestContextT,
    create_task_request_data: RequestDataT,  # Create task request data
    regular_presentation_handler: HandlerT,
) -> None:
    """Test *create task* handler action completed successfully."""
    assert (
        regular_presentation_handler.execute(
            mock_request_params,
            request_context,
            create_task_request_data,
        )
    ) is not None


@pytest.mark.django_db
def test_update_progress(
    translations: list[TaskItem],
    mock_request_params: RequestParamsT,
    request_context: RequestContextT,
    update_progress_request_data: RequestDataT,  # Update progress request data
    mock_user_command_storage: Mock,
    main_container: MainContainer,
) -> None:
    """Test *update progress* handler action completed successfully."""
    # Arrange
    # The study item ID for progress update is stored.
    mock_user_command_storage.retrieve.return_value = (
        PresentationExerciseDomainResult(
            status=ExerciseStatus.NEW_TASK,
            item=translations[0],
        )
    )

    # Act
    with main_container.lang.use_cases.user_command_storage.override(  # type: ignore[attr-defined]
        mock_user_command_storage
    ):
        handler = (
            main_container.lang.handlers.regular_translation_presentation()  # type: ignore[attr-defined]
        )
        result = handler.execute(
            mock_request_params,
            request_context,
            update_progress_request_data,
        )

        # Assert
        mock_user_command_storage.retrieve.assert_called_once()
        assert result is not None
