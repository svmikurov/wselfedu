"""Test exercise response adapters."""

from typing import override

from ports.contract.entity.general import NullProtocol
from ports.interfaces.protocols.use_case.exercise import (
    TestUseCaseResultProtocol,
)
from ports.interfaces.schemas.web.task import (
    TestExerciseTaskResponse,
    TestTaskContext,
)

from ..base import BaseWebAdapter


class WebTestExerciseAdapter(
    BaseWebAdapter[
        TestUseCaseResultProtocol,
        NullProtocol,
        TestExerciseTaskResponse,
    ],
):
    """Web test exercise response adapter."""

    # FIXME: Fix type ignore
    @override
    def to_response(
        self,
        use_case_result: TestUseCaseResultProtocol,
        request_context: NullProtocol,
    ) -> TestExerciseTaskResponse:
        """Convert domain result to web representation context."""
        context = TestTaskContext(
            question_text=use_case_result.task.question_text,
            options=use_case_result.task.options,  # type: ignore
        )
        return TestExerciseTaskResponse(
            domain_status=use_case_result.status,
            context=context,
        )
