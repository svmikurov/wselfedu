"""Test exercise response adapters."""

from typing import Any, Iterable, TypeVar, override

from contracts import NullProtocol
from contracts.entity.domain.exercise.fields import ExerciseCaseProtocol
from contracts.schemas.domain.exercise.flow import TestExerciseTask
from interfaces.schemas.web.task import (
    Option,
    TestExerciseTaskResponse,
    TestTaskContext,
)

from ..base import BaseWebAdapter

ExtraContextT = TypeVar('ExtraContextT', bound=Iterable[Any])


class WebTestExerciseAdapter(
    BaseWebAdapter[
        ExerciseCaseProtocol[TestExerciseTask[list[Option]]],
        NullProtocol,
        TestExerciseTaskResponse,
    ],
):
    """Web test exercise response adapter."""

    # HACK: Update return type hint on protocol
    @override
    def to_response(
        self,
        # FIXME: Fix type hint
        use_case_result: ExerciseCaseProtocol[TestExerciseTask[list[Option]]],
        request_context: NullProtocol,
    ) -> TestExerciseTaskResponse:
        """Convert domain result to web representation context."""
        context = TestTaskContext(
            question_text=use_case_result.domain.question_text,
            options=use_case_result.domain.items,
        )
        return TestExerciseTaskResponse(
            domain_status=use_case_result.status,
            context=context,
        )
