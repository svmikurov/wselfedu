"""Test exercise response adapters."""

from typing import Any, Generic, TypeAlias, TypeVar, override

from django.template.loader import render_to_string

from apps.core.adapters.response.abstract import AbstractResponseAdapter
from apps.core.adapters.response.status import ResponseStatusEnum
from apps.core.domains.exercise.test.dto import TestExerciseCase
from apps.lang.models import EnglishTranslation
from contracts import NullProtocol
from contracts.entity.response.base import OobResponseProtocol
from contracts.enums import ExerciseStatus
from contracts.schemas.response import TestExerciseTaskResponse
from contracts.schemas.response.generic import OobResponseDTO

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
        TestExerciseTaskResponse[EnglishTranslation],
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
    def to_response(  # type: ignore
        self,
        domain_result: TestExerciseCase[ExtraContext],
        request_context: NullProtocol,
    ) -> OobResponseProtocol[T]:
        """Convert domain result to web representation context."""
        return TestExerciseTaskResponse(  # type: ignore
            domain_status=ExerciseStatus.NEW_TASK,
            context=domain_result,  # type: ignore
        )


class WebExplainAdapter(
    AbstractResponseAdapter[
        TestExerciseCase[ExtraContext],
        NullProtocol,
        OobResponseProtocol[TestExerciseCase[ExtraContext]],
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

    def _build_oob(self, domain_result: TestExerciseCase[ExtraContext]) -> str:
        """Build OOB."""
        html = ''
        for template in self._templates:
            html += render_to_string(template, domain_result.model_dump())
        return html

    @override
    def to_response(
        self,
        domain_result: TestExerciseCase[ExtraContext],
        request_context: NullProtocol,
    ) -> OobResponseProtocol[TestExerciseCase[ExtraContext]]:
        """Convert domain result to web representation context."""
        return OobResponseDTO(
            domain_status=ResponseStatusEnum.EXPLAIN_CASE,  # type: ignore
            context=domain_result,
            oob_html=self._build_oob(domain_result),
        )
