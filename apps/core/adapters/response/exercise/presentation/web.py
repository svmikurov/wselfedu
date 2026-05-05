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
"""Partial Out-Of-Band HTML template.
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
        oob_templates: list[_HTML],
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the adapter."""
        super().__init__(name=name, auditor=auditor)
        self._oob_templates = oob_templates

    def _get_oob_html(self, context: PresentationTaskContext) -> _HTML:
        """Build Out-Of-Band HTML."""
        oob_htmls: list[str] = []
        for template in self.oob_templates:
            oob_htmls.append(render_to_string(template, context.model_dump()))
        return '\n'.join(oob_htmls)

    @property
    def oob_templates(self) -> list[_HTML]:
        """Return Out-Of-Band HTML templates."""
        return self._oob_templates

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
            oob_html=(
                self._get_oob_html(context) if request_context.is_htmx else ''
            ),
        )
