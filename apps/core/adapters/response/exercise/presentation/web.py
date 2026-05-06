"""Generic exercise response adapters.

This module contains adapters for converting generic
exercise cases to different output formats (API and Web).
"""

from typing import TypeAlias, override

from django.template.loader import render_to_string

from apps.core.adapters.response.abstract import AbstractResponseAdapter
from contracts.enums import ExerciseStatus
from contracts.schemas.domain.exercise.flow import PresentationTask
from interfaces.protocols.request import HasIsHtmx
from interfaces.schemas.web.task import (
    PresentationTaskContext,
    PresentationTaskResponse,
)
from utils.audit.base import BaseAuditable
from utils.audit.protocol import AuditorProtocol

_HTML: TypeAlias = str
"""Partial HTML template.
"""


class PresentationTaskWebAdapter(
    BaseAuditable,
    AbstractResponseAdapter[
        PresentationTask,
        HasIsHtmx,
        PresentationTaskResponse,
    ],
):
    """WEB adapter for perform exercise task."""

    def __init__(
        self,
        templates: list[_HTML],
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the adapter."""
        super().__init__(name=name, auditor=auditor)
        self._templates = templates

    def _get_html(self, context: PresentationTaskContext) -> _HTML:
        """Build partial HTMLs."""
        html: list[str] = []
        for template in self.templates:
            html.append(render_to_string(template, context.model_dump()))
        return '\n'.join(html)

    @property
    def templates(self) -> list[_HTML]:
        """Return partial HTML templates."""
        return self._templates

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
