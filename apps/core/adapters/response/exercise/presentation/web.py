"""Presentation exercise task WEB adapter."""

from typing import override

from contracts.entity.domain.exercise.fields import ExerciseCaseProtocol
from contracts.schemas.domain.exercise.flow import PresentationTask
from interfaces.protocols.request import HasIsHtmx
from interfaces.schemas.web.task import (
    PresentationTaskContext,
    PresentationTaskResponse,
)

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
        domain_result: ExerciseCaseProtocol[PresentationTask],
        request_context: HasIsHtmx,
    ) -> PresentationTaskResponse:
        """Convert exercise case to web context."""
        context = PresentationTaskContext(
            define=domain_result.domain.question_text,
            mean=domain_result.domain.answer_text,
            progress_value=domain_result.domain.progress_value,
        )
        return PresentationTaskResponse(
            domain_status=domain_result.status,
            context=context,
            html=(self._get_html(context) if request_context.is_htmx else ''),
        )
