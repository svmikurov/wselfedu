"""Generic exercise response adapters.

This module contains adapters for converting generic
exercise cases to different output formats (API and Web).
"""

from typing import override

from django.template.loader import render_to_string

from apps.core.adapters.response.abstract import AbstractResponseAdapter
from interfaces import NullProtocol
from interfaces.enums import ExerciseStatus
from interfaces.protocols.response.exercise import (
    PresentationTaskResponse,
)
from interfaces.schemas.domain.exercise.presentation import (
    PresentationTask,
)


class PresentationTaskWebAdapter(
    AbstractResponseAdapter[
        PresentationTask,
        NullProtocol,
        PresentationTaskResponse,
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

    @override
    def to_response(
        self,
        domain_result: PresentationTask,
        request_context: NullProtocol,
    ) -> PresentationTaskResponse:
        """Convert exercise case to web context."""
        return PresentationTaskResponse(
            domain_status=ExerciseStatus.NEW_TASK,
            context=domain_result,
            oob_html=self._build_oob(domain_result),
        )
