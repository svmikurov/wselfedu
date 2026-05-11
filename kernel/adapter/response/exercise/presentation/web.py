"""Presentation exercise task WEB adapter."""

from typing import override

from ports.interfaces.protocols.service.exercise import (
    ExerciseCaseProtocol
)
from ports.interfaces.protocols.domain.exercise import (
    ExerciseDomainResultProtocol
)
from ports.contract.entity.general import HasIsHtmx
from ports.interfaces.schemas.domain.exercise.flow import PresentationTask
from ports.interfaces.schemas.web.task import (
    PresentationTaskContext,
    PresentationTaskResponse,
)

from ..base import BaseWebAdapter

ExerciseCaseT = ExerciseCaseProtocol[
    ExerciseDomainResultProtocol, PresentationTask
]


class PresentationTaskWebAdapter(
    BaseWebAdapter[
        ExerciseCaseT,
        HasIsHtmx,
        PresentationTaskResponse,
    ],
):
    """WEB adapter for exercise task."""

    # HACK: Update return type hint to protocol
    @override
    def to_response(
        self,
        use_case_result: ExerciseCaseT,
        request_context: HasIsHtmx,
    ) -> PresentationTaskResponse:
        """Convert exercise case to web context."""
        context = PresentationTaskContext(
            define=use_case_result.task.question_text,
            mean=use_case_result.task.answer_text,
            progress_value=use_case_result.task.progress_value,
        )
        return PresentationTaskResponse(
            domain_status=use_case_result.status,
            context=context,
            html=(self._get_html(context) if request_context.is_htmx else ''),
        )
