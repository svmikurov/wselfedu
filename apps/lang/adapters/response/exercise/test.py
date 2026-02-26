"""Test exercise response adapters."""

from __future__ import annotations

from typing import TYPE_CHECKING

from apps.core.domains.exercise import (
    ExerciseStatusEnum,
    TestExerciseData,
    TestExerciseExplanation,
)
from apps.lang.schemas.test import (
    Explanation,
    TestCase,
    TestResponseData,
)

if TYPE_CHECKING:
    from apps.lang.schemas import Explanation, TestCase


class WebTestAdapter:
    """Web test exercise response adapter.

    Converts domain data to web-ready format.
    """

    # HACK: Fix signature and implementation
    @classmethod
    def to_response(
        cls, case: TestExerciseData | Explanation
    ) -> TestResponseData:
        """Convert domain result to web representation context."""
        match case.status:
            case ExerciseStatusEnum.NEW_CASE:
                if not isinstance(case, TestExerciseData):
                    raise ValueError('Unexpected case type')
                data = TestCase(
                    case_uuid=str(case.case_uuid),
                    question=case.question_text,
                    options=case.answer_text_options,
                )

            case ExerciseStatusEnum.EXPLAIN:
                if not isinstance(case, TestExerciseExplanation):
                    raise ValueError('Unexpected type')
                data = Explanation(
                    case_question=case.question_text,
                    case_answer=case.answer_text,
                    selected_answer=case.selected_question_text,
                    selected_question=case.selected_answer_text,
                )

            case _:
                raise ValueError('Unsupported case status')

        return TestResponseData(status=case.status, data=data)
