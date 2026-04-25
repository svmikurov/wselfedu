"""Domain logic for selecting items for test exercise cases."""

from random import randrange, sample

from apps.core.domains.exercise.test.dto import OptionMetaDTO
from apps.core.exceptions import info
from interfaces.aliases import CandidatesAlias
from interfaces.enums.exercise import DisplayOrder
from interfaces.protocols.domain import exercise

from ..abstract import (
    AbstractCheckExerciseDomain,
    AbstractConfigurableCandidatesExerciseDomain,
)
from ..deps.protocol import SelectorProtocol
from ..dto import TextExerciseCheckResult
from ..protocol import (
    HasOptionValue,
)
from .dto import TestDomainResult, TestExerciseMeta
from .protocol import TestExerciseCaseProtocol

__all__ = [
    'TestDomain',
    'TestExerciseCheckDomain',
]


class _ExerciseConfig(
    exercise.HasDisplayOrder[DisplayOrder],
    exercise.HasOptionCount,
):
    """Exercise config interface."""


class TestDomain(
    AbstractConfigurableCandidatesExerciseDomain[
        _ExerciseConfig,
        TestExerciseCaseProtocol,
    ],
):
    """Task exercise case domain."""

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
    ) -> TestExerciseCaseProtocol:
        """Get test exercise data."""
        option_value = randrange(conf.option_count)
        selected_candidates = self._selector.select(candidates, conf)
        options = self._get_options(selected_candidates, conf.option_count)

        return TestDomainResult(
            value=option_value,
            options=options,
        )

    def _get_options(
        self,
        candidates: CandidatesAlias,
        option_count: int,
    ) -> list[exercise.Candidate]:
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
        HasOptionValue,
        TestExerciseMeta[OptionMetaDTO],
        TextExerciseCheckResult,
    ],
):
    """Test exercise check user's answer domain business logic."""

    def execute(
        self,
        answer: HasOptionValue,
        case_meta: TestExerciseMeta[OptionMetaDTO],
    ) -> TextExerciseCheckResult:
        """Check user's answer."""
        raise NotImplementedError
