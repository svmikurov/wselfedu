"""Domain logic for selecting items for test exercise cases."""

from random import randrange, sample

from apps.core.exceptions import info
from ports.abstract.domain.exercise import (
    AbstractCandidatesExerciseDomain,
    AbstractCheckExerciseDomain,
)
from ports.contract import enums
from ports.contract.entity.domain.exercise.fields import (
    HasDisplayOrder,
    HasOptionCount,
)
from ports.contract.entity.domain.exercise.flow import TestDomainResultProtocol
from ports.contract.entity.domain.general import HasCheckResult
from ports.contract.infra.domain.selector import SelectorProtocol
from ports.interfaces.protocols.domain.exercise import (
    CandidatesT,
    TaskItemsT,
    TestAnswerProtocol,
)
from ports.interfaces.schemas.domain.exercise.exercise import (
    CheckTaskResult,
    TestTaskDomainResult,
)
from utils.audit.base import BaseAuditable

__all__ = [
    'TestDomain',
    'TestExerciseCheckDomain',
]


class _ExerciseConfig(
    HasDisplayOrder[enums.DisplayOrder],
    HasOptionCount,
):
    """Exercise config interface."""


class TestDomain(
    AbstractCandidatesExerciseDomain[
        _ExerciseConfig,
        TestDomainResultProtocol,
    ],
):
    """Task exercise case domain."""

    __test__ = False

    def __init__(
        self,
        selector: SelectorProtocol[_ExerciseConfig],
    ) -> None:
        """Configure the domain."""
        self._selector = selector

    def execute(
        self,
        candidates: CandidatesT,
        conf: _ExerciseConfig,
    ) -> TestDomainResultProtocol:
        """Get test exercise data."""
        option_value = randrange(conf.option_count)
        selected_candidates = self._selector.select(candidates, conf)
        options = self._get_options(selected_candidates, conf.option_count)

        return TestTaskDomainResult(
            status=enums.ExerciseStatus.NEW_TASK,
            question_option_value=option_value,
            items=options,  # type: ignore
        )

    def _get_options(
        self,
        candidates: CandidatesT,
        option_count: int,
    ) -> TaskItemsT:
        """Get test exercise options."""
        if len(candidates) >= option_count:
            return sample(tuple(candidates), option_count)
        else:
            raise info.NoExerciseItemsException('Not enough candidates')


# =================================================
# Check
# =================================================


class TestExerciseCheckDomain(
    BaseAuditable,
    AbstractCheckExerciseDomain[
        TestAnswerProtocol,
        TestDomainResultProtocol,
        HasCheckResult,
    ],
):
    """Test exercise check user's answer domain business logic."""

    def execute(
        self,
        answer: TestAnswerProtocol,
        case: TestDomainResultProtocol,
    ) -> HasCheckResult:
        """Check user's answer."""
        # HACK: Fix persistent domain result.
        return CheckTaskResult(
            status=enums.ExerciseStatus.CORRECT,
            is_correct=True,
        )
