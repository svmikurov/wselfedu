"""Language discipline translation presentation exercise DI tests."""

from unittest.mock import Mock

import pytest

from apps.core.storages.services.iabc import AbstractCommandStorage
from contracts.enums import ExerciseStatus
from di import MainContainer
from interfaces.schemas.domain.exercise import (
    PresentationExerciseDomainResult,
    TaskItem,
)

from .._types.handler import (
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
    main_container: MainContainer,
) -> None:
    """Test *update progress* handler action completed successfully."""
    # Arrange
    # The study item ID for progress update is stored.
    mock_domain_result_storage = Mock(spec=AbstractCommandStorage)
    mock_domain_result_storage.name = 'test_task'
    mock_domain_result_storage.retrieve.return_value = (
        PresentationExerciseDomainResult(
            status=ExerciseStatus.NEW_TASK,
            item=translations[0],
        )
    )

    # Act
    with main_container.lang.use_cases.user_command_storage.override(  # type: ignore[attr-defined]
        mock_domain_result_storage
    ):
        handler = (
            main_container.lang.handlers.regular_translation_presentation()  # type: ignore[attr-defined]
        )
        result = handler.execute(
            null_request_params,
            user_request_context,
            update_progress_request_data,
        )

        # Assert
        mock_domain_result_storage.retrieve.assert_called_once()
        assert result is not None
