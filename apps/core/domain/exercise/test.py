"""Domain logic for selecting items for test exercise cases."""

from __future__ import annotations

from random import randrange, sample
from typing import TYPE_CHECKING

from apps.core.exceptions import info

from .abstract import (
    AbstractCandidatesExerciseDomain,
    AbstractCheckExerciseDomain,
    AbstractSettingsExerciseDomain,
)
from .enums import DisplayOrder
from .test_dto import (
    Option,
    OptionMeta,
    TestExerciseCase,
    TestExerciseMeta,
    TestExerciseResult,
)
from .types import Settings

type Result = tuple[TestExerciseCase, TestExerciseMeta]

if TYPE_CHECKING:
    from .types import (
        Candidate,
        Candidates,
        CheckResult,
        ExerciseConfig,
        TestCheckRequest,
    )

    type Options = list[Candidate]

__all__ = [
    'DetailTestCreateDomain',
    'RegularTestCreateDomain',
    'TestCheckDomain',
]

MAX_OPTION_COUNT = 7
MIN_OPTION_COUNT = 2

QUESTION_INDEX = 0
ANSWER_INDEX = 1


class _BaseTestCreateDomain:
    """ABC for test exercise domain create case business logic."""

    def __init__(self, config: ExerciseConfig) -> None:
        """Configure the domain."""
        self._option_count: int = config.option_count
        self._item_count: int = config.item_count
        self._phases_order: DisplayOrder = config.display_order

    def _execute(self, candidates: Candidates) -> Result:
        """Get test exercise data."""
        limited_candidates = self._get_limited(candidates)
        options = self._get_options(limited_candidates)
        question_option_value = randrange(self._option_count)
        # The order of the display case phases may be random.
        ordered_phases = self._phases_order.get_display_phases()

        case = self._build_case(options, question_option_value, ordered_phases)
        meta = self._build_meta(options, question_option_value, ordered_phases)
        return case, meta

    def _get_limited(self, candidates: Candidates) -> Candidates:
        """Limit candidates for exercise."""
        # Temporary returns first database query items
        # TODO: Implement candidates limit order
        # after additional processing by service
        return candidates.order_by('id')[: self._item_count]

    def _build_case(
        self, options: Options, value: int, phases: list[str]
    ) -> TestExerciseCase:
        """Build exercise case DTO to rendering."""
        return TestExerciseCase(
            question_text=self._get_question(options[value], phases),
            answer_text_options=[
                Option(value=index, text=self._get_answer(option, phases))
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
                OptionMeta(
                    pk=option.pk,
                    value=index,
                    define=option.define,
                    explain=option.explain,
                )
                for index, option in enumerate(options)
            ],
        )

    def _get_options(self, candidates: Candidates) -> Options:
        """Get test exercise options."""
        if len(candidates) >= self._option_count:
            return sample(tuple(candidates), self._option_count)
        else:
            raise info.NoExerciseItemsException('Not enough translations')

    def _get_question(self, candidate: Candidate, phases: list[str]) -> str:
        """Get question text by display case phase order."""
        return getattr(candidate, phases[QUESTION_INDEX])  # type: ignore

    def _get_answer(self, candidate: Candidate, phases: list[str]) -> str:
        """Get answer text by display case phase order."""
        return getattr(candidate, phases[ANSWER_INDEX])  # type: ignore


class RegularTestCreateDomain(
    _BaseTestCreateDomain,
    AbstractSettingsExerciseDomain[Settings, Result],
):
    """Regular test exercise domain create case business logic."""

    def execute(self, candidates: Candidates, settings: Settings) -> Result:
        """Get test exercise data."""
        self._set_exercise_configuration(settings)
        return self._execute(candidates)

    def _set_exercise_configuration(self, settings: Settings) -> None:
        """Set test exercise configuration."""
        if (
            hasattr(settings, 'option_count')
            and isinstance(settings.option_count, int)
            and MAX_OPTION_COUNT <= settings.option_count <= MAX_OPTION_COUNT
        ):
            self._option_count = settings.option_count
        if (
            hasattr(settings, 'item_count')
            and isinstance(settings.item_count, int)
            and self._option_count <= settings.item_count
        ):
            self._item_count = settings.item_count
        if hasattr(settings, 'display_order') and isinstance(
            settings.display_order, DisplayOrder
        ):
            self._phases_order = settings.display_order


class DetailTestCreateDomain(
    _BaseTestCreateDomain,
    AbstractCandidatesExerciseDomain[Result],
):
    """Detail test exercise domain create case business logic."""

    def execute(self, candidates: Candidates) -> Result:
        """Get test exercise data."""
        return self._execute(candidates)


class TestCheckDomain(AbstractCheckExerciseDomain[TestExerciseMeta]):
    """Test exercise check user's answer domain business logic."""

    def execute(
        self,
        answer: TestCheckRequest,
        case_meta: TestExerciseMeta,
    ) -> CheckResult:
        """Check user's answer."""
        print('****************************************')
        print(f'{answer = }')
        print(f'{case_meta = }')
        print('****************************************')
        is_correct = case_meta.option_value == answer.option_value
        return TestExerciseResult(
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
