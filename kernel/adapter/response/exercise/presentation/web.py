"""Presentation exercise task WEB adapter."""

from typing import override

from ports.contract.entity.general import HasIsHtmx
from ports.contract.enums import ExerciseStatus
from ports.interfaces.protocols.domain.exercise import PresentationTaskProtocol
from ports.interfaces.schemas.web.task import (
    PresentationTaskContext,
    PresentationTaskResponse,
)

from ..base import BaseWebAdapter


class CreatePresentationWebAdapter(
    BaseWebAdapter[
        PresentationTaskProtocol,
        HasIsHtmx,
        PresentationTaskResponse,
    ],
):
    """WEB adapter for create exercise presentation task."""

    # HACK: Update return type hint to protocol
    @override
    def to_response(
        self,
        use_case_result: PresentationTaskProtocol,
        request_context: HasIsHtmx,
    ) -> PresentationTaskResponse:
        """Convert exercise case to web context."""
        context = PresentationTaskContext(
            define=use_case_result.question_text,
            mean=use_case_result.answer_text,
            progress_value=use_case_result.progress_value,
        )
        return PresentationTaskResponse(
            domain_status=ExerciseStatus.NEW_TASK,
            context=context,
            html=(self._get_html(context) if request_context.is_htmx else ''),
        )
