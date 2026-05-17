"""Test exercise hendler DI "smoke" tests."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from ports.contract.enums import ExerciseAction, ExerciseStatus
from ports.interfaces.request.web.exercise import CheckTestData
from ports.interfaces.schemas.base import NullDTO
from ports.interfaces.schemas.domain.exercise.exercise import (
    TestTaskDomainResult,
)
from ports.interfaces.schemas.request.handler import RequestData
from tests.fixtures.exercise.lang.no_db.translations import (
    TASK_ITEMS,
    TRANSLATION_INDEX,
)

if TYPE_CHECKING:
    from di import MainContainer
    from ports.contract.types.handler import TestHandlerT
    from ports.interfaces.protocols.handler.exercise import CreateRequestDataT
    from ports.interfaces.protocols.request.general import (
        RequestContextProtocol,
    )
    from ports.interfaces.schemas.domain.exercise.exercise import TaskItem


@pytest.mark.django_db
def test_create_presentation_task(
    translations: list[TaskItem],  # populate DB
    test_handler: TestHandlerT,
    request_context: RequestContextProtocol,
    create_task_request_data: CreateRequestDataT,
) -> None:
    """Test presentation request handler smoke."""
    # Act
    try:
        result = test_handler.execute(
            params=NullDTO(),
            context=request_context,
            data=create_task_request_data,
        )
    except Exception as exp:
        pytest.fail(f'Create test task test fail: {exp}')

    # Assert
    assert result is not None


@pytest.mark.parametrize(
    'correct_option_value, user_answer_option_value',
    (
        (TRANSLATION_INDEX, str(TRANSLATION_INDEX)),
        (TRANSLATION_INDEX, str(TRANSLATION_INDEX + 1)),
    ),
)
@pytest.mark.django_db
def test_check_correct_user_test_answer(
    correct_option_value: int,
    user_answer_option_value: str,
    mock_user_command_storage: Mock,
    request_context: RequestContextProtocol,
    main_container: MainContainer,
) -> None:
    """Test the check correct answer request handler smoke."""
    # Arrange
    mock_user_command_storage.retrieve.return_value = TestTaskDomainResult(
        question_option_value=correct_option_value,
        items=TASK_ITEMS,
        status=ExerciseStatus.NEW_TASK,
    )

    # Act
    with main_container.lang.use_cases.user_command_storage.override(  # type: ignore[attr-defined]
        mock_user_command_storage
    ):
        handler = (
            main_container.lang.handlers.regular_translation_test()  # type: ignore[attr-defined]
        )
        try:
            result = handler.execute(
                params=NullDTO(),
                context=request_context,
                data=RequestData[CheckTestData](
                    data={
                        'action': ExerciseAction.CHECK_ANSWER,
                        'option_value': user_answer_option_value,
                    },
                ),
            )
        except Exception as exp:
            pytest.fail(f'Check user answer test task failed: {exp}')

        # Assert
        mock_user_command_storage.retrieve.assert_called_once()
        assert result is not None
