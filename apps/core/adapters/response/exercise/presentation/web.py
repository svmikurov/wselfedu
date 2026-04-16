"""Generic exercise response adapters.

This module contains adapters for converting generic
exercise cases to different output formats (API and Web).
"""

from typing import TypeVar, override

from django.template.loader import render_to_string
from pydantic import BaseModel

from apps.core.adapters.response.abstract import AbstractResponseAdapter
from apps.core.adapters.response.dto import OobResponseDTO
from apps.core.adapters.response.status import ResponseStatusEnum
from apps.core.contracts import NullProtocol
from apps.core.domains.null import NullDTO

DomainResult = TypeVar('DomainResult', bound=BaseModel)


class WebStartExerciseNullAdapter(
    AbstractResponseAdapter[
        DomainResult,
        NullProtocol,
        OobResponseDTO[ResponseStatusEnum, DomainResult, NullDTO],
    ]
):
    """WEB adapter for start web exercise.

    Passes original domain result DTO via response DTO.
    """

    def __init__(
        self,
        extra_oob_templates: list[str],
    ) -> None:
        """Construct the adapter."""
        self._templates = extra_oob_templates

    def _build_oob(self, domain_result: DomainResult) -> str:
        """Build OOB."""
        html = ''
        for template in self._templates:
            html += render_to_string(template, domain_result.model_dump())
        return html

    @override
    def to_response(
        self,
        domain_result: DomainResult,
        request_context: NullProtocol,
    ) -> OobResponseDTO[ResponseStatusEnum, DomainResult, NullDTO]:
        """Convert exercise case to web context."""
        return OobResponseDTO(
            status=ResponseStatusEnum.NEW_CASE,
            # NOTE: Passes original domain result.
            context=domain_result,
            oob_html=self._build_oob(domain_result),
        )
