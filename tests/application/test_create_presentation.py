"""Task use case test."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from wse.application.use_case import CreateTaskUseCase
from wse.domain.services.task import CreatePresentationService

if TYPE_CHECKING:
    from wse.application.abstract import AbstractCreateTaskUseCase
    from wse.domain.protocols import (
        CandidatesRepositoryProtocol,
        CreateTaskServiceProtocol,
        Presentable,
    )


@pytest.fixture
def presentation_domain() -> CreateTaskServiceProtocol[Presentable]:
    """Provide a create presentation task service."""
    return CreatePresentationService()


@pytest.fixture
def presentation_use_case(
    candidates_fake_repo: CandidatesRepositoryProtocol,
    presentation_domain: CreateTaskServiceProtocol[Presentable],
) -> CreateTaskUseCase[Presentable]:
    """Provide a create presentation task use case."""
    return CreateTaskUseCase(
        repository=candidates_fake_repo,
        domain=presentation_domain,
    )


def test_create_task_use_case(
    presentation_use_case: AbstractCreateTaskUseCase[Presentable],
) -> None:
    # Act
    task = presentation_use_case.execute()

    # Assert
    # - that task created
    assert task is not None
    # - that task has attributes
    assert hasattr(task, 'question_text')
    assert hasattr(task, 'answer_text')
    # - that task attributes is text
    assert isinstance(task.question_text, str)
    assert isinstance(task.answer_text, str)
