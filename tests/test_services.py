"""Application use case test."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from wse.application.use_case import CreateTaskUseCase
from wse.domain.services.task import CreateTaskService

from .fake.repository import FakeCandidatesRepository

if TYPE_CHECKING:
    from wse.domain.protocols import (
        CandidatesRepositoryProtocol,
        CreateTaskServiceProtocol,
        Learnable,
    )


@pytest.fixture
def fake_repository() -> CandidatesRepositoryProtocol:
    """Provide a task candidates repository."""
    return FakeCandidatesRepository()


@pytest.fixture
def domain() -> CreateTaskServiceProtocol:
    """Provide a create the task domain service."""
    return CreateTaskService()


@pytest.fixture
def use_case(
    fake_repository: CandidatesRepositoryProtocol,
    domain: CreateTaskServiceProtocol,
) -> CreateTaskUseCase:
    """Provide a create task service."""
    return CreateTaskUseCase(repository=fake_repository, domain=domain)


def test_create_task_service(
    use_case: CreateTaskUseCase,
    candidates: list[Learnable],
) -> None:
    # Act
    task = use_case.execute()

    # Assert
    # - that task created
    assert task is not None
    assert task in candidates
    # - that task has attributes
    assert hasattr(task, 'define')
    assert hasattr(task, 'explain')
