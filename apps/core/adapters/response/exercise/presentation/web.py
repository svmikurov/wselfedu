"""Generic exercise response adapters.

This module contains adapters for converting generic
exercise cases to different output formats (API and Web).
"""

from typing import override

from django.template.loader import render_to_string

from apps.core.adapters.response.abstract import AbstractResponseAdapter
from contracts import NullProtocol
from contracts.enums import ExerciseStatus
from contracts.schemas.domain.exercise.flow import PresentationTask
from interfaces.schemas import web as interfaces


class PresentationTaskWebAdapter(
    AbstractResponseAdapter[
        PresentationTask,
        NullProtocol,
        interfaces.PresentationTaskResponse,
    ]
):
    """WEB adapter for perform exercise task."""

    def __init__(
        self,
        extra_oob_templates: list[str],
    ) -> None:
        """Construct the adapter."""
        self._templates = extra_oob_templates

    def _build_oob(self, domain_result: PresentationTask) -> str:
        """Build OOB."""
        html = ''
        for template in self._templates:
            html += render_to_string(template, domain_result.model_dump())
        return html

    # HACK: Update return type hint on protocol
    @override
    def to_response(
        self,
        domain_result: PresentationTask,
        request_context: NullProtocol,
    ) -> interfaces.PresentationTaskResponse:
        """Convert exercise case to web context."""
        return interfaces.PresentationTaskResponse(
            domain_status=ExerciseStatus.NEW_TASK,
            context=interfaces.PresentationTaskSchema(
                define=domain_result.question_text,
                mean=domain_result.answer_text,
                progress_value=domain_result.progress_value,
            ),
            oob_html=self._build_oob(domain_result),
        )
