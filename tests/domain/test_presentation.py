"""Presentation exercise tests."""

from typing import TypeVar
from unittest.mock import Mock

import pytest

from tests.fixtures.exercise import SESSION_ID
from wse.domain.factories import PresentationFactory
from wse.domain.protocols import Executable, PresentationTaskProtocol

SpecificationT = TypeVar('SpecificationT')


@pytest.fixture
def create_strategy(
    presentation_task: PresentationTaskProtocol,
) -> Mock:
    """Provide a create presentation task strategy."""
    mock = Mock(spec=Executable)
    mock.execute.return_value = presentation_task
    return mock


def test_presentation_factory_creates_task_with_question_and_answer(
    create_strategy: Executable[SpecificationT, PresentationTaskProtocol],
) -> None:
    # Arrange
    factory = PresentationFactory(create_strategy=create_strategy)
    presentation = factory.create(session_id=SESSION_ID)

    # Act
    task = presentation.create()

    # Assert: task exists and has required attributes
    assert task is not None
    assert isinstance(task.question_text, str)
    assert isinstance(task.answer_text, str)
