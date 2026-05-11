"""Test exercise response adapters."""

from typing import Any, Iterable, TypeVar, override

from ports.contract.entity.general import NullProtocol
from ports.interfaces.protocols.service.exercise import TestTaskProtocol
from ports.interfaces.schemas.web.task import (
    TestExerciseTaskResponse,
    TestTaskContext,
)

from ..base import BaseWebAdapter

ExtraContextT = TypeVar('ExtraContextT', bound=Iterable[Any])


class WebTestExerciseAdapter(
    BaseWebAdapter[
        TestTaskProtocol,
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
        use_case_result: TestTaskProtocol,
        request_context: NullProtocol,
    ) -> TestExerciseTaskResponse:
        """Convert domain result to web representation context."""
        context = TestTaskContext(
            question_text=use_case_result.question_text,
            options=use_case_result.items,
        )
        return TestExerciseTaskResponse(
            domain_status=use_case_result.status,
            context=context,
        )
