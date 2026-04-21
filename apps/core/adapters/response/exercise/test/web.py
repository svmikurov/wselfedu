"""Test exercise response adapters."""

from typing import Any, Generic, TypeAlias, TypeVar, override

from django.template.loader import render_to_string

from apps.core.adapters.response.abstract import AbstractResponseAdapter
from apps.core.adapters.response.status import ResponseStatusEnum
from apps.core.contracts import NullProtocol
from apps.core.contracts.response.web import OobResponseDTO
from apps.core.domains.exercise.test.dto import TestExerciseCase

ExtraContext = TypeVar('ExtraContext')
T = TypeVar('T')

_ResponseDTO: TypeAlias = OobResponseDTO[
    ResponseStatusEnum,
    TestExerciseCase[ExtraContext],
    ExtraContext,
]


class WebTestExerciseAdapter(
    AbstractResponseAdapter[
        TestExerciseCase[ExtraContext],
        NullProtocol,
        _ResponseDTO[ExtraContext],
    ],
    Generic[ExtraContext],
):
    """Web test exercise response adapter.

    Returns response DTO.
    """

    def __init__(
        self,
        extra_oob_templates: list[str],
    ) -> None:
        """Construct the adapter."""
        self._templates = extra_oob_templates

    def _build_oob(self, context: dict[str, Any]) -> str:
        """Build OOB."""
        html = ''
        for template in self._templates:
            html += render_to_string(template, context)
        return html

    @override
    def to_response(
        self,
        domain_result: TestExerciseCase[ExtraContext],
        request_context: NullProtocol,
    ) -> _ResponseDTO[ExtraContext]:
        """Convert domain result to web representation context."""
        return OobResponseDTO(
            domain_status=ResponseStatusEnum.NEW_CASE,
            context=domain_result,
        )


class WebExplainAdapter(
    AbstractResponseAdapter[
        TestExerciseCase[ExtraContext],
        NullProtocol,
        _ResponseDTO[ExtraContext],
    ],
):
    """Web test exercise explain response adapter.

    Returns response DTO.
    """

    def __init__(
        self,
        extra_oob_templates: list[str],
    ) -> None:
        """Construct the adapter."""
        self._templates = extra_oob_templates

    def _build_oob(self, context: dict[str, Any]) -> str:
        """Build OOB."""
        html = ''
        for template in self._templates:
            html += render_to_string(template, context)
        return html

    @override
    def to_response(
        self,
        domain_result: TestExerciseCase[ExtraContext],
        request_context: NullProtocol,
    ) -> _ResponseDTO[ExtraContext]:
        """Convert domain result to web representation context."""
        return OobResponseDTO(
            domain_status=ResponseStatusEnum.EXPLAIN_CASE,
            context=domain_result,
        )
