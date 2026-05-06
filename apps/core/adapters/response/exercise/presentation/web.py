"""Presentation exercise task WEB adapter."""

from typing import override

from contracts.enums import ExerciseStatus
from contracts.schemas.domain.exercise.flow import PresentationTask
from interfaces.protocols.request import HasIsHtmx
from interfaces.schemas.web.task import (
    PresentationTaskContext,
    PresentationTaskResponse,
)

from ..base import BaseWebAdapter


class PresentationTaskWebAdapter(
    BaseWebAdapter[
        PresentationTask,
        HasIsHtmx,
        PresentationTaskResponse,
    ],
):
    """WEB adapter for exercise task."""

    # HACK: Update return type hint to protocol
    @override
    def to_response(
        self,
        domain_result: PresentationTask,
        request_context: HasIsHtmx,
    ) -> PresentationTaskResponse:
        """Convert exercise case to web context."""
        context = PresentationTaskContext(
            define=domain_result.question_text,
            mean=domain_result.answer_text,
            progress_value=domain_result.progress_value,
        )
        return PresentationTaskResponse(
            domain_status=ExerciseStatus.NEW_TASK,
            context=context,
            html=(self._get_html(context) if request_context.is_htmx else ''),
        )
