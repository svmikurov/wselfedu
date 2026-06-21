"""Testing use case tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from wse.application import commands, use_cases
from wse.domain import services
from wse.infrastructure import repository

if TYPE_CHECKING:
    from wse.application.protocols import (
        CerateTestingCommandProto,
        CheckResultDtoProto,
        CheckTestingCommandProto,
        Executable,
        TaskDtoProto,
    )
    from wse.domain.protocols import (
        AnswerCheckable,
        ExerciseCreatable,
        HasIdentifier,
        HasSessionIdentifier,
        Repository,
        Testable,
        UniqueLearnable,
    )


###################################################
# Fixtures
###################################################


# Tested use cases dependencies: Domain services


@pytest.fixture
def create_service() -> ExerciseCreatable:
    """Provide a create testing task domain service."""
    return services.CreateTestingService()


@pytest.fixture
def check_service() -> AnswerCheckable:
    """Provide a check testing answer domain service."""
    return services.CheckTestingService()


# Tested use cases dependencies: Repositories


@pytest.fixture
def learnable_repo(
    learnables: list[UniqueLearnable],
) -> Repository[int, HasIdentifier]:
    """Provide a learnables repository."""
    repo = repository.InMemoryLearnableRepository()
    for item in learnables:
        repo.add(item)
    return repo


@pytest.fixture
def task_repo() -> Repository[str, HasSessionIdentifier]:
    """Provide a task repository."""
    return repository.InMemoryTaskRepository()


# Tested use cases


@pytest.fixture
def create_use_case(
    learnable_repo: Repository[int, UniqueLearnable],
    create_service: ExerciseCreatable,
) -> Executable[CerateTestingCommandProto, TaskDtoProto[Testable]]:
    """Provide a create testing task use case."""
    return use_cases.CreateTestingUseCase(learnable_repo, create_service)


@pytest.fixture
def check_use_case(
    task_repo: Repository[str, TaskDtoProto[Testable]],
    check_service: AnswerCheckable,
) -> Executable[CheckTestingCommandProto, CheckResultDtoProto]:
    """Provide a create testing task use case."""
    return use_cases.CheckTestingUseCase(task_repo, check_service)


# Task


@pytest.fixture
def task(create_use_case: Executable) -> TaskDtoProto[Testable]:
    """Provide a testing task."""
    create_cmd = commands.CreateTestingTask(
        session_id='test session',
    )
    return create_use_case.execute(cmd=create_cmd)


###################################################
# Tests
###################################################


def test_testing_task_created_with_attribute_types(
    task: TaskDtoProto[Testable],
) -> None:
    # Assert
    assert task is not None
    assert task.task is not None
    assert isinstance(task.session_id, str)


def test_checked_correct_testing_answer(
    task: TaskDtoProto[Testable],
    task_repo: Repository[str, HasSessionIdentifier],
    check_use_case: Executable,
) -> None:
    # Arrange
    correct_answer = task.task.question_value
    check_cmd = commands.CheckTestingAnswer(
        session_id=task.session_id,
        answer_value=correct_answer,
    )
    task_repo.add(task)

    # Act
    result = check_use_case.execute(check_cmd)

    # Assert
    assert result is not None
    assert result.is_correct is True


def test_checked_incorrect_testing_answer(
    task: TaskDtoProto[Testable],
    task_repo: Repository[str, HasSessionIdentifier],
    check_use_case: Executable,
) -> None:
    # Arrange
    check_cmd = commands.CheckTestingAnswer(
        session_id=task.session_id,
        answer_value=1 if task.task.question_value != 1 else 2,
    )
    task_repo.add(task)

    # Act
    result = check_use_case.execute(check_cmd)

    # Assert
    assert result is not None
    assert result.is_correct is False
