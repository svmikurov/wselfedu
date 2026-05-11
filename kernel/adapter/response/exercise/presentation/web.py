"""Presentation exercise task WEB adapter."""

from typing import override

from interfaces.schemas.web.task import (
    PresentationTaskContext,
    PresentationTaskResponse,
)
from ports.contract.entity.domain.exercise.fields import ExerciseCaseProtocol
from ports.contract.entity.general import HasIsHtmx
from ports.interfaces.schemas.domain.exercise.flow import PresentationTask

from ..base import BaseWebAdapter


class PresentationTaskWebAdapter(
    BaseWebAdapter[
        ExerciseCaseProtocol[PresentationTask],
        HasIsHtmx,
        PresentationTaskResponse,
    ],
):
    """WEB adapter for exercise task."""

    # HACK: Update return type hint to protocol
    @override
    def to_response(
        self,
        use_case_result: ExerciseCaseProtocol[PresentationTask],
        request_context: HasIsHtmx,
    ) -> PresentationTaskResponse:
        """Convert exercise case to web context."""
        context = PresentationTaskContext(
            define=use_case_result.domain.question_text,
            mean=use_case_result.domain.answer_text,
            progress_value=use_case_result.domain.progress_value,
        )
        return PresentationTaskResponse(
            domain_status=use_case_result.status,
            context=context,
            html=(self._get_html(context) if request_context.is_htmx else ''),
        )
