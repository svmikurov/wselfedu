"""Application layer pytest configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generator
from unittest.mock import Mock

import pytest

from tests.factories.mock import (
    create_learnable_repo_mock,
    create_task_repo_mock,
)
from tests.factories.model import (
    CORRECT_ANSWER_OPTION_VALUE,
    INCORRECT_ANSWER_OPTION_VALUE,
    TASK_SESSION_ID,
)
from wse.application import commands, dto

if TYPE_CHECKING:
    from wse.application.protocols import (
        CerateTestingCommandProto,
        CheckTestingCommandProto,
        TaskDtoProto,
    )
    from wse.di.application import ApplicationContainer
    from wse.domain.protocols import Testable, UniqueLearnable


###################################################
# Command fixtures
###################################################


@pytest.fixture
def command_create_testing() -> CerateTestingCommandProto:
    """Provide a check testing task command."""
    return commands.CreateTestingTask(session_id=TASK_SESSION_ID)


@pytest.fixture
def command_check_testing_with_correct_answer() -> CheckTestingCommandProto:
    """Provide a check testing answer command with correct answer."""
    return commands.CheckTestingAnswer(
        session_id=TASK_SESSION_ID,
        answer_value=CORRECT_ANSWER_OPTION_VALUE,
    )


@pytest.fixture
def command_check_testing_with_incorrect_answer() -> CheckTestingCommandProto:
    """Provide a check testing answer command with incorrect answer."""
    return commands.CheckTestingAnswer(
        session_id=TASK_SESSION_ID,
        answer_value=INCORRECT_ANSWER_OPTION_VALUE,
    )


###################################################
# DTO fixtures
###################################################


@pytest.fixture
def testing_task_dto(
    testing_task: Testable,
) -> TaskDtoProto:
    """Provide a testing task DTO."""
    return dto.Task(task=testing_task, session_id=TASK_SESSION_ID)


###################################################
# Repository mock fixtures
###################################################


@pytest.fixture
def mock_learnable_repo(learnables: tuple[UniqueLearnable, ...]) -> Mock:
    """Provide a learnable repository mock with added learnables."""
    return create_learnable_repo_mock(learnables)


@pytest.fixture
def mock_task_repo(testing_task_dto: TaskDtoProto) -> Mock:
    """Provide a task repository mock."""
    return create_task_repo_mock(testing_task_dto)


###################################################
# DI Container fixture
###################################################


@pytest.fixture
def container_with_mocks_for_task_execution(
    mock_learnable_repo: Mock,
    mock_task_repo: Mock,
    container: ApplicationContainer,
) -> Generator[ApplicationContainer, None, None]:
    """Provide a DI container with mocked repo for task execution."""
    with (
        container.repositories.learnable.override(mock_learnable_repo),
        container.repositories.task.override(mock_task_repo),
    ):
        yield container
