"""Domain logic for selecting items for test exercise cases."""

from random import randrange, sample

from apps.core.domains.exercise.test.dto import OptionMetaDTO
from apps.core.exceptions import info
from contracts import enums
from contracts.entity.domain.exercise.fields import (
    HasDisplayOrder,
    HasOptionCount,
    HasQuestionOptionValue,
)
from contracts.entity.domain.exercise.flow import TestDomainResultProtocol
from interfaces.protocols.domain.exercise import (
    CandidatesProtocol,
    TaskItemsProtocol,
)
from interfaces.schemas.domain.exercise import TestExerciseDomainResult

from ..abstract import (
    AbstractCheckExerciseDomain,
    AbstractConfigurableCandidatesExerciseDomain,
)
from ..deps.protocol import SelectorProtocol
from ..dto import TextExerciseCheckResult
from .dto import TestExerciseMeta

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
    AbstractConfigurableCandidatesExerciseDomain[
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
        candidates: CandidatesProtocol,
        conf: _ExerciseConfig,
    ) -> TestDomainResultProtocol:
        """Get test exercise data."""
        option_value = randrange(conf.option_count)
        selected_candidates = self._selector.select(candidates, conf)
        options = self._get_options(selected_candidates, conf.option_count)

        return TestExerciseDomainResult(
            status=enums.ExerciseStatus.NEW_TASK,
            question_option_value=option_value,
            items=options,  # type: ignore
        )

    def _get_options(
        self,
        candidates: CandidatesProtocol,
        option_count: int,
    ) -> TaskItemsProtocol:
        """Get test exercise options."""
        if len(candidates) >= option_count:
            return sample(tuple(candidates), option_count)
        else:
            raise info.NoExerciseItemsException('Not enough candidates')


# =================================================
# Check
# =================================================


class TestExerciseCheckDomain(
    AbstractCheckExerciseDomain[
        HasQuestionOptionValue,
        TestExerciseMeta[OptionMetaDTO],
        TextExerciseCheckResult,
    ],
):
    """Test exercise check user's answer domain business logic."""

    def execute(
        self,
        answer: HasQuestionOptionValue,
        case_meta: TestExerciseMeta[OptionMetaDTO],
    ) -> TextExerciseCheckResult:
        """Check user's answer."""
        raise NotImplementedError
