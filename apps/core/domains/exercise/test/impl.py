"""Domain logic for selecting items for test exercise cases."""

from random import randrange, sample

from apps.core.exceptions import info

from ..abstract import (
    AbstractCheckExerciseDomain,
    AbstractConfigurableCandidatesExerciseDomain,
)
from ..dto import TextExerciseCheckResult
from ..protocol import (
    Candidate,
    Candidates,
    HasDisplayOrder,
    SelectorProtocol,
)
from .dto import (
    OptionDTO,
    OptionMetaDTO,
    TestExerciseCase,
    TestExerciseMeta,
)
from .protocol import HasOptionCount, HasOptionValue

__all__ = [
    'TestExerciseCreateDomain',
    'TestExerciseCheckDomain',
]


type Options = list[Candidate]


class _ExerciseConfig(
    HasDisplayOrder,
    HasOptionCount,
):
    """Exercise config interface."""


MAX_OPTION_COUNT = 7
MIN_OPTION_COUNT = 2

QUESTION_INDEX = 0
ANSWER_INDEX = 1

# =================================================
# Create
# =================================================


class TestExerciseCreateDomain(
    AbstractConfigurableCandidatesExerciseDomain[
        _ExerciseConfig,
        tuple[TestExerciseCase, TestExerciseMeta],
    ],
):
    """ABC for test exercise domain create case business logic."""

    def __init__(
        self,
        selector: SelectorProtocol[_ExerciseConfig],
    ) -> None:
        """Configure the domain."""
        self._selector = selector

    def execute(
        self,
        candidates: Candidates,
        conf: _ExerciseConfig,
    ) -> tuple[TestExerciseCase, TestExerciseMeta]:
        """Get test exercise data."""
        option_count = conf.option_count
        selected_candidates = self._selector.select(candidates, conf)

        options = self._get_options(selected_candidates, option_count)
        question_option_value = randrange(option_count)
        ordered_phases = conf.display_order.get_display_phases()

        case = self._build_case(options, question_option_value, ordered_phases)
        meta = self._build_meta(options, question_option_value, ordered_phases)
        return case, meta

    def _build_case(
        self,
        options: Options,
        value: int,
        phases: list[str],
    ) -> TestExerciseCase:
        """Build exercise case DTO to rendering."""
        return TestExerciseCase(
            question_text=self._get_question(options[value], phases),
            answer_text_options=[
                OptionDTO(
                    option_value=int(index),
                    text=self._get_answer(option, phases),
                )
                for index, option in enumerate(options)
            ],
        )

    def _build_meta(
        self, options: Options, value: int, phases: list[str]
    ) -> TestExerciseMeta:
        """Build exercise case metadata DTO for internal tracking."""
        return TestExerciseMeta(
            pk=options[value].pk,
            question_text=self._get_question(options[value], phases),
            answer_text=self._get_answer(options[value], phases),
            option_value=value,
            options=[
                OptionMetaDTO(
                    pk=option.pk,
                    option_value=index,
                    define=option.define,
                    explain=option.explain,
                )
                for index, option in enumerate(options)
            ],
        )

    def _get_options(
        self, candidates: Candidates, option_count: int
    ) -> Options:
        """Get test exercise options."""
        if len(candidates) >= option_count:
            return sample(tuple(candidates), option_count)
        else:
            raise info.NoExerciseItemsException('Not enough translations')

    def _get_question(self, candidate: Candidate, phases: list[str]) -> str:
        """Get question text by display case phase order."""
        return getattr(candidate, phases[QUESTION_INDEX])  # type: ignore

    def _get_answer(self, candidate: Candidate, phases: list[str]) -> str:
        """Get answer text by display case phase order."""
        return getattr(candidate, phases[ANSWER_INDEX])  # type: ignore


# =================================================
# Check
# =================================================


class TestExerciseCheckDomain(
    AbstractCheckExerciseDomain[
        HasOptionValue,
        TestExerciseMeta,
        TextExerciseCheckResult,
    ],
):
    """Test exercise check user's answer domain business logic."""

    def execute(
        self,
        answer: HasOptionValue,
        case_meta: TestExerciseMeta,
    ) -> TextExerciseCheckResult:
        """Check user's answer."""
        is_correct = case_meta.option_value == answer.option_value
        return TextExerciseCheckResult(
            is_correct=is_correct,
            question_text=case_meta.question_text,
            answer_text=case_meta.answer_text,
            selected_question_text=case_meta.get_question_text(
                answer.option_value
            ),
            selected_answer_text=case_meta.get_answer_text(
                answer.option_value
            ),
        )
