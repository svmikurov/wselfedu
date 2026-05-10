"""Test exercise domain tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from ports.contract.enums import ExerciseStatus
from ports.interfaces.schemas.domain.exercise.exercise import (
    CheckTaskResult,
    TestAnswer,
)
from tests.fixtures.exercise.lang.no_db.translations import (
    TEST_TASK_DOMAIN_RESULT,
    TRANSLATION_INDEX,
)

if TYPE_CHECKING:
    from di import MainContainer
    from kernel.domain.exercise.test import TestExerciseCheckDomain
    from ports.contract.infra.domain.exercise import CheckTaskDomainProtocol
    from ports.interfaces.protocols.domain import (
        CheckTestAnswerDomainResultProtocol,
        TestAnswerProtocol,
    )


@pytest.fixture
def domain_check(
    main_container: MainContainer,
) -> TestExerciseCheckDomain:
    """Provide the check user test answer domain."""
    return main_container.core.domains.check_test()  # type: ignore


@pytest.mark.parametrize(
    'answer, case, expected',
    (
        (
            TestAnswer(option_value=TRANSLATION_INDEX),
            TEST_TASK_DOMAIN_RESULT,
            CheckTaskResult(status=ExerciseStatus.CORRECT, is_correct=True),
        ),
        (
            TestAnswer(option_value=TRANSLATION_INDEX + 1),
            TEST_TASK_DOMAIN_RESULT,
            CheckTaskResult(status=ExerciseStatus.WRONG, is_correct=False),
        ),
    ),
)
def test_check_domain(
    answer: TestAnswerProtocol,
    case: TestAnswerProtocol,
    expected: CheckTestAnswerDomainResultProtocol,
    domain_check: CheckTaskDomainProtocol[
        TestAnswerProtocol,
        TestAnswerProtocol,
        CheckTestAnswerDomainResultProtocol,
    ],
) -> None:
    """Test domain."""
    assert domain_check.execute(answer, case) == expected
