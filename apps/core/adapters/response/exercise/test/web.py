"""Test exercise response adapters."""

from typing import Any, Generic, Iterable, TypeAlias, TypeVar, override

from django.template.loader import render_to_string

from apps.core.adapters.response.abstract import AbstractResponseAdapter
from apps.core.adapters.response.status import ResponseStatusEnum
from apps.core.domains.exercise.test.dto import TestExerciseCase
from contracts import NullProtocol
from contracts.entity.response.base import OobResponseProtocol
from contracts.schemas.domain.exercise.flow import TestExerciseTask
from contracts.schemas.response.generic import OobResponseDTO
from interfaces.schemas.domain.exercise import Option
from interfaces.schemas.web import task as interfaces
from utils.audit.base import BaseAuditable
from utils.audit.protocol import AuditorProtocol

ExtraContext = TypeVar('ExtraContext', bound=Iterable[Any])
T = TypeVar('T')

_ResponseDTO: TypeAlias = OobResponseDTO[
    ResponseStatusEnum,
    TestExerciseCase[ExtraContext],
    ExtraContext,
]


class WebTestExerciseAdapter(
    BaseAuditable,
    AbstractResponseAdapter[
        TestExerciseTask[list[Option]],
        NullProtocol,
        interfaces.TestExerciseTaskResponse,
    ],
    Generic[ExtraContext],
):
    """Web test exercise response adapter.

    Returns response DTO.
    """

    def __init__(
        self,
        extra_oob_templates: list[str],
        *args: object,
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
        **kwargs: object,
    ) -> None:
        """Construct the adapter."""
        super().__init__(name=name, auditor=auditor)
        self._templates = extra_oob_templates

    def _build_oob(self, context: dict[str, Any]) -> str:
        """Build OOB."""
        html = ''
        for template in self._templates:
            html += render_to_string(template, context)
        return html

    # HACK: Update return type hint on protocol
    @override
    def to_response(
        self,
        domain_result: TestExerciseTask[list[Option]],
        request_context: NullProtocol,
    ) -> interfaces.TestExerciseTaskResponse:
        """Convert domain result to web representation context."""
        return interfaces.TestExerciseTaskResponse(
            domain_status=domain_result.status,
            context=interfaces.TestTaskSchema(
                question=domain_result.options[
                    domain_result.question_option_value
                ].text,
                options=domain_result.options,
            ),
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
            context=interfaces.TestTaskSchema(
                question=domain_result.question_text,
                options=[
                    Option(
                        value=option.options_value,
                        text=option.text,
                    )
                    for option in domain_result.options
                ],
            ),
            oob_html=self._build_oob(domain_result),
        )
