"""Factories for mock."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

from wse.domain.protocols import Repository

if TYPE_CHECKING:
    from wse.application.protocols import TaskDtoProto
    from wse.domain.protocols import UniqueLearnable


def create_learnable_repo_mock(
    learnables: tuple[UniqueLearnable, ...],
) -> Mock:
    """Create a learnable repository mock."""
    repo = Mock(spec=Repository)
    repo.list.return_value = learnables
    return repo


def create_task_repo_mock(testing_task_dto: TaskDtoProto) -> Mock:
    """Create a task repository mock."""
    repo = Mock(spec=Repository)
    repo.get.return_value = testing_task_dto
    return repo
