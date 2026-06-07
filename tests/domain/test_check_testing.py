"""Test of testing answer check service."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from wse.domain.services.task import CheckTestingService
from wse.domain.values import AnswerCheck

if TYPE_CHECKING:
    from wse.domain.protocols import (
        AnswerCheckableService,
        CheckableOption,
        HasCorrect,
    )


@pytest.fixture
def service() -> AnswerCheckableService[CheckableOption, HasCorrect]:
    """Provide check testing task answer service."""
    return CheckTestingService()


@pytest.mark.parametrize(
    'question_option_value, answer_option_value, is_correct',
    ((3, 3, True), (3, 4, False)),
    ids=['correct answer', 'incorrect_answer'],
)
def test_check_answer(
    question_option_value: int,
    answer_option_value: int,
    is_correct: bool,
    service: AnswerCheckableService[CheckableOption, HasCorrect],
) -> None:
    # Arrange
    answer = AnswerCheck(question_option_value, answer_option_value)

    # Act
    result = service.execute(answer)

    # Assert
    assert result.is_correct is is_correct
