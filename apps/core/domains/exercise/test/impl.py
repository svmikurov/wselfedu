"""Domain logic for selecting items for test exercise cases."""

from random import randrange, sample

from apps.core.domains.exercise.test.dto import OptionMetaDTO
from apps.core.exceptions import info
from contracts import enums
from contracts.aliases import CandidatesAlias
from contracts.entity.domain.exercise.fields import (
    HasDisplayOrder,
    HasOptionCount,
    HasQuestionOptionValue,
)
from contracts.entity.domain.exercise.flow import TestDomainResultProtocol
from contracts.schemas.domain.exercise.flow import TestExerciseDomainResult
from interfaces.protocols.domain.exercise import Candidates

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
        candidates: CandidatesAlias,
        conf: _ExerciseConfig,
    ) -> TestDomainResultProtocol:
        """Get test exercise data."""
        option_value = randrange(conf.option_count)
        selected_candidates = self._selector.select(candidates, conf)
        options = self._get_options(selected_candidates, conf.option_count)

        return TestExerciseDomainResult(
            status=enums.ExerciseStatus.NEW_TASK,
            question_option_value=option_value,
            options=options,
        )

    def _get_options(
        self,
        candidates: CandidatesAlias,
        option_count: int,
    ) -> Candidates:
        """Get test exercise options."""
        if len(candidates) >= option_count:
            # FIXME: Fix type hint
            return sample(tuple(candidates), option_count)  # type: ignore
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
