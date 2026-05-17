"""Presentation exercise hendler DI "smoke" tests."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from ports.contract.enums import ExerciseStatus
from ports.interfaces.schemas.base import NullDTO
from ports.interfaces.schemas.domain.exercise.exercise import (
    PresentationTaskDomainResult,
)

if TYPE_CHECKING:
    from di import MainContainer
    from ports.contract.types.handler import PresentationHandlerT
    from ports.interfaces.protocols.handler.exercise import (
        CreateRequestDataT,
        UpdateProgressRequestDataT,
    )
    from ports.interfaces.protocols.request.general import (
        RequestContextProtocol,
    )
    from ports.interfaces.schemas.domain.exercise.exercise import TaskItem


@pytest.mark.django_db
def test_create_presentation_task(
    translations: list[TaskItem],  # populate DB
    presentation_handler: PresentationHandlerT,
    request_context: RequestContextProtocol,
    create_task_request_data: CreateRequestDataT,
) -> None:
    """Test presentation request handler smoke."""
    # Act
    try:
        result = presentation_handler.execute(
            params=NullDTO(),
            context=request_context,
            data=create_task_request_data,
        )
    except Exception as exp:
        pytest.fail(f'Create presentation task test fail: {exp}')

    # Assert
    assert result is not None


@pytest.mark.django_db
def test_update_progress_presentation_task(
    translations: list[TaskItem],  # populate DB
    mock_user_command_storage: Mock,
    request_context: RequestContextProtocol,
    update_progress_request_data: UpdateProgressRequestDataT,
    main_container: MainContainer,
) -> None:
    """Test update progress presentation request handler smoke."""
    # Arrange
    mock_user_command_storage.retrieve.return_value = (
        PresentationTaskDomainResult(
            item=translations[0],
            status=ExerciseStatus.NEW_TASK,
        )
    )

    # Act
    with main_container.lang.use_cases.user_command_storage.override(  # type: ignore[attr-defined]
        mock_user_command_storage
    ):
        handler = (
            main_container.lang.handlers.regular_translation_presentation()  # type: ignore[attr-defined]
        )
        try:
            result = handler.execute(
                params=NullDTO(),
                context=request_context,
                data=update_progress_request_data,
            )
        except Exception as exp:
            pytest.fail(f'Update progress presentation task test fail: {exp}')

        # Assert
        mock_user_command_storage.retrieve.assert_called_once()
        assert result is not None
