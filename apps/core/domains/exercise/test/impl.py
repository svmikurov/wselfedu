"""Domain logic for selecting items for test exercise cases."""

from random import randrange, sample

from apps.core.domains.exercise.test.dto import OptionMetaDTO
from apps.core.exceptions import info
from interfaces import enums
from interfaces.aliases import CandidatesAlias
from interfaces.entity.domain.exercise import fields, flow
from interfaces.schemas.domain.exercise import dtos

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
    fields.HasDisplayOrder[enums.DisplayOrder],
    fields.HasOptionCount,
):
    """Exercise config interface."""


class TestDomain(
    AbstractConfigurableCandidatesExerciseDomain[
        _ExerciseConfig,
        flow.TestDomainResultProtocol,
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
    ) -> flow.TestDomainResultProtocol:
        """Get test exercise data."""
        option_value = randrange(conf.option_count)
        selected_candidates = self._selector.select(candidates, conf)
        options = self._get_options(selected_candidates, conf.option_count)

        return dtos.TestTask[fields.Candidates](
            option_value=option_value,
            options=options,
        )

    def _get_options(
        self,
        candidates: CandidatesAlias,
        option_count: int,
    ) -> fields.Candidates:
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
        fields.HasQuestionOptionValue,
        TestExerciseMeta[OptionMetaDTO],
        TextExerciseCheckResult,
    ],
):
    """Test exercise check user's answer domain business logic."""

    def execute(
        self,
        answer: fields.HasQuestionOptionValue,
        case_meta: TestExerciseMeta[OptionMetaDTO],
    ) -> TextExerciseCheckResult:
        """Check user's answer."""
        raise NotImplementedError
