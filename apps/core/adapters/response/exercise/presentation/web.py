"""Generic exercise response adapters.

This module contains adapters for converting generic
exercise cases to different output formats (API and Web).
"""

import logging
from typing import TypeAlias, override

from django.template.loader import render_to_string

from apps.core.adapters.response.abstract import AbstractResponseAdapter
from contracts import NullProtocol
from contracts.enums import ExerciseStatus
from contracts.schemas.domain.exercise.flow import PresentationTask
from interfaces.schemas import web as interfaces

log = logging.getLogger(__name__)

_Template: TypeAlias = str
"""Partial html template.
"""


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
        extra_oob_templates: list[_Template],
        template_registry: dict[ExerciseStatus, list[_Template]] | None = None,
    ) -> None:
        """Construct the adapter."""
        self._templates = extra_oob_templates
        self._template_registry = template_registry

    def _build_oob(self, domain_result: PresentationTask) -> _Template:
        """Build OOB."""
        templates: list[_Template] = self._get_templates(domain_result.status)
        context = domain_result.model_dump()

        htmls: list[str] = []
        for template in templates:
            htmls.append(render_to_string(template, context))

        return '\n'.join(htmls)

    def _get_templates(self, status: ExerciseStatus) -> list[_Template]:
        """Return partial templates for response."""
        if not self._template_registry:
            return self._templates

        try:
            status_templates = self._template_registry[status]
        except KeyError:
            log.warning(
                'Web response adapter template registry ',
                f'have no templates for {status}',
            )
        else:
            status_templates = []

        return self._templates + status_templates

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
            context=interfaces.PresentationTaskContext(
                define=domain_result.question_text,
                mean=domain_result.answer_text,
                progress_value=domain_result.progress_value,
            ),
            oob_html=self._build_oob(domain_result),
        )
