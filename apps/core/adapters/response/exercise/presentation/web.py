"""Presentation exercise response adapters.

This module contains adapters for converting Presentation
exercise cases to different output formats (API and Web).
"""

from typing import Any, override

from django.template.loader import render_to_string

from apps.core.adapters.response.abstract import AbstractResponseAdapter
from apps.core.adapters.response.dto import OobResponseDTO
from apps.core.adapters.response.status import StatusEnum
from apps.core.domains.exercise.presentation.dto import PresentationCase
from apps.core.domains.null import NullDTO
from apps.core.domains.protocol import NullProtocol

_WebPresentationAdapter = AbstractResponseAdapter[
    PresentationCase,
    NullProtocol,
    OobResponseDTO[StatusEnum, PresentationCase, NullDTO],
]


class WebPresentationAdapter(_WebPresentationAdapter):
    """WEB adapter for Presentation exercise type.

    Converts domain DTO to Web response format.
    Includes extra context needed for server-rendered templates.
    """

    def __init__(
        self,
        template_names: list[str],
    ) -> None:
        """Construct the adapter."""
        self._template_names = template_names

    def _build_oob(self, context: dict[str, Any]) -> str:
        """Build OOB."""
        html = ''
        for template_name in self._template_names:
            html += render_to_string(template_name, context)
        return html

    @override
    def to_response(
        self,
        context: PresentationCase,
        extra_context: NullProtocol,
    ) -> OobResponseDTO[StatusEnum, PresentationCase, NullDTO]:
        """Convert Presentation case to web context."""
        return OobResponseDTO(
            status=StatusEnum.NEW_CASE,
            context=context,
            oob_html=self._build_oob(context.model_dump()),
        )
