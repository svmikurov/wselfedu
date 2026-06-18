"""Testing use case tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from wse.application import commands, use_cases
from wse.domain import services
from wse.infrastructure import repository

if TYPE_CHECKING:
    from wse.application.protocols import CerateTestingCommandProto, Executable
    from wse.domain.protocols import (
        ExerciseCreatable,
        Repository,
        UniqueLearnable,
    )


@pytest.fixture
def repo(learnables: list[UniqueLearnable]) -> Repository:
    """Provide learnables repository."""
    repo = repository.InMemoryRepository()
    for item in learnables:
        repo.add(item)
    return repo


@pytest.fixture
def service() -> ExerciseCreatable:
    """Provide a create testing domain service."""
    return services.CreateTestingService()


@pytest.fixture
def create_use_case(
    repo: Repository,
    service: ExerciseCreatable,
) -> Executable:
    """Provide a create testing task use case."""
    return use_cases.CreateTestingUseCase(repo, service)


@pytest.fixture
def create_cmd() -> CerateTestingCommandProto:
    """Provide a create testing task command."""
    return commands.CreateTestingTask()


def test_create_testing_task(
    create_use_case: Executable,
    create_cmd: CerateTestingCommandProto,
) -> None:
    # Act
    task = create_use_case.execute(create_cmd)

    # Assert
    assert task is not None
